"""Testes de confirmação de email e do serviço SMTP.

Cobertura:
    - criação, verificação e expiração de tokens de confirmação
    - marcação de token como confirmado
    - inicialização do serviço SMTP
    - comportamento sem credenciais SMTP
"""

import asyncio
import pytest
from typing import cast, Any
import sqlite3
from app.services.confirmacao_email_service import ConfirmacaoEmailService
from app.database.local import Database as SQLiteDatabase, SQLiteConnection, SQLiteCursor
from app.services.email_service import EmailService


class MinimalTestDatabase:
    """Banco de dados mínimo para testes sem o schema completo."""
    
    def __init__(self):
        self._connection = sqlite3.connect(":memory:")
        self._connection.row_factory = sqlite3.Row
    
    @staticmethod
    def _context_connection(connection):
        """Context manager para conexão."""
        class _Ctx:
            def __enter__(self):
                return SQLiteConnection(connection)
            def __exit__(self, *args):
                pass
        return _Ctx()
    
    def connect(self):
        """Retorna conexão SQLite."""
        return self._context_connection(self._connection)


class DummyRequest:
    def __init__(self):
        self.session = {}


class TestConfirmacaoEmailService:
    """Testes para o serviço de confirmação de email."""

    def setup_method(self):
        """Executado antes de cada teste."""
        self.db = MinimalTestDatabase()
        
        # Criar somente a tabela necessária para os testes do token
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE confirmacao_email (
                    id_confirmacao INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_usuario INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    token_hash TEXT NOT NULL UNIQUE,
                    expira_em TEXT NOT NULL,
                    confirmado INTEGER DEFAULT 0,
                    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
        self.confirmacao_service = ConfirmacaoEmailService(cast(Any, self.db))

    def test_criar_token_confirmacao(self):
        """Cria o token de confirmação e assegura que não seja vazio."""
        email = "usuario@example.com"
        usuario_id = 1
        
        token = self.confirmacao_service.criar_token_confirmacao(email, usuario_id)
        
        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)

    def test_verificar_token_valido(self):
        """Verifica se um token recém-criado é considerado válido."""
        email = "usuario@example.com"
        usuario_id = 1
        
        token = self.confirmacao_service.criar_token_confirmacao(email, usuario_id)
        resultado = self.confirmacao_service.verificar_token(token)
        
        assert resultado is not None
        assert resultado["email"] == email
        assert resultado["id_usuario"] == usuario_id
        assert resultado["token_hash"] is not None

    def test_verificar_token_invalido(self):
        """Verifica que um token inválido retorna None."""
        token_invalido = "token_invalido_xyz"
        resultado = self.confirmacao_service.verificar_token(token_invalido)
        
        assert resultado is None

    def test_marcar_como_confirmado(self):
        """Marca token como confirmado e garante que não possa ser reutilizado."""
        email = "usuario@example.com"
        usuario_id = 1
        
        token = self.confirmacao_service.criar_token_confirmacao(email, usuario_id)
        resultado = self.confirmacao_service.verificar_token(token)
        
        assert resultado is not None
        token_hash = resultado["token_hash"]
        
        # Marcar como confirmado
        marcado = self.confirmacao_service.marcar_como_confirmado(token_hash)
        assert marcado is True
        
        # Verificar que o token não é mais válido
        resultado_apos = self.confirmacao_service.verificar_token(token)
        assert resultado_apos is None

    def test_token_expira(self):
        """Valida que tokens com data de expiração anterior são rejeitados."""
        email = "usuario@example.com"
        usuario_id = 1
        
        token = self.confirmacao_service.criar_token_confirmacao(email, usuario_id)
        
        # Simular expiração do token (mover a data de expiração para o passado)
        with self.confirmacao_service.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE confirmacao_email SET expira_em = ? WHERE email = ?",
                ("2020-01-01 00:00:00", email)
            )
        
        # Tentar verificar token expirado
        resultado = self.confirmacao_service.verificar_token(token)
        assert resultado is None

    def test_multiplos_tokens_diferentes_usuarios(self):
        """Confirma que tokens distintos são gerados para usuários diferentes."""
        email1 = "usuario1@example.com"
        email2 = "usuario2@example.com"
        usuario_id1 = 1
        usuario_id2 = 2
        
        token1 = self.confirmacao_service.criar_token_confirmacao(email1, usuario_id1)
        token2 = self.confirmacao_service.criar_token_confirmacao(email2, usuario_id2)
        
        # Tokens devem ser diferentes
        assert token1 != token2
        
        # Cada token deve retornar seu usuário correto
        resultado1 = self.confirmacao_service.verificar_token(token1)
        resultado2 = self.confirmacao_service.verificar_token(token2)
        
        assert resultado1 is not None
        assert resultado2 is not None
        assert resultado1["id_usuario"] == usuario_id1
        assert resultado1["email"] == email1
        assert resultado2["id_usuario"] == usuario_id2
        assert resultado2["email"] == email2


class TestEmailService:
    """Testes para o serviço de email SMTP."""

    def test_email_service_inicializa(self):
        """Verifica a inicialização do EmailService com configuração do ambiente."""
        service = EmailService()
        
        assert service.smtp_server is not None
        assert service.smtp_port > 0
        # sender_email e sender_password podem ser None em testes

    def test_email_service_sem_credenciais(self):
        """Verifica que o envio falha quando não há credenciais SMTP."""
        service = EmailService()
        
        # Simular credenciais vazias
        service.sender_email = None
        service.sender_password = None
        # A função é assíncrona, então executamos o envio no teste com asyncio
        resultado = asyncio.run(service.enviar_email("destino@example.com", "Teste", "<p>Teste</p>", "Teste"))
        assert resultado is False
