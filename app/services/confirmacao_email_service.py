import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.services.email_service import EmailService


class ConfirmacaoEmailService:
    """Gerencia tokens e confirmação de email para novos usuários."""

    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db
        self.email_service = EmailService()
        self.TOKEN_EXPIRY_MINUTES = 24 * 60  # 24 horas
        self.SESSION_KEY = "email_confirmations"

    def _gerar_token(self) -> str:
        """Gera um token seguro e aleatório."""
        return secrets.token_urlsafe(32)

    def _hash_token(self, token: str) -> str:
        """Hash SHA256 do token para armazenamento seguro."""
        return hashlib.sha256(token.encode()).hexdigest()

    def _agora(self) -> datetime:
        """Retorna a data/hora atual em UTC."""
        return datetime.now(timezone.utc)

    def criar_token_confirmacao(self, email: str, usuario_id: int) -> str:
        """
        Cria um token de confirmação para um email.
        
        Args:
            email: Email do usuário
            usuario_id: ID do usuário
        
        Returns:
            Token de confirmação (deve ser enviado por email)
        """
        token = self._gerar_token()
        token_hash = self._hash_token(token)
        expira_em = self._agora() + timedelta(minutes=self.TOKEN_EXPIRY_MINUTES)

        with self.db.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO confirmacao_email 
                    (id_usuario, email, token_hash, expira_em, confirmado)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (usuario_id, email, token_hash, expira_em, False)
                )
            except Exception as e:
                print(f"Erro ao criar token de confirmação: {e}")
                raise

        return token

    async def enviar_email_confirmacao(
        self, 
        email: str, 
        nome: str, 
        token: str,
        url_base: str = "http://localhost:8000"
    ) -> bool:
        """
        Envia email de confirmação para o usuário.
        
        Args:
            email: Email do destinatário
            nome: Nome do usuário
            token: Token de confirmação
            url_base: URL base da aplicação
        
        Returns:
            True se enviado com sucesso
        """
        link_confirmacao = f"{url_base}/confirmar-email?token={token}"

        corpo_html = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <h2>Bem-vindo à Crimson Claw Studio!</h2>
                <p>Olá {nome},</p>
                <p>Obrigado por se registrar. Clique no link abaixo para confirmar seu email:</p>
                <p>
                    <a href="{link_confirmacao}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                        Confirmar Email
                    </a>
                </p>
                <p>Ou copie e cole este link no seu navegador:</p>
                <p>{link_confirmacao}</p>
                <p>Este link expira em 24 horas.</p>
                <hr>
                <p><small>Se você não criou esta conta, ignore este email.</small></p>
            </body>
        </html>
        """

        corpo_texto = f"""
        Bem-vindo à Crimson Claw Studio!
        
        Olá {nome},
        
        Obrigado por se registrar. Confirme seu email clicando no link:
        {link_confirmacao}
        
        Este link expira em 24 horas.
        
        Se você não criou esta conta, ignore este email.
        """

        return await self.email_service.enviar_email(
            email,
            "Confirme seu Email - Crimson Claw Studio",
            corpo_html,
            corpo_texto
        )

    def verificar_token(self, token: str) -> dict | None:
        """
        Verifica e valida um token de confirmação.
        
        Args:
            token: Token a ser verificado
        
        Returns:
            Dict com dados do usuário se válido, None caso contrário
        """
        token_hash = self._hash_token(token)
        agora = self._agora()

        with self.db.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    SELECT id_usuario, email, confirmado, expira_em
                    FROM confirmacao_email
                    WHERE token_hash = %s
                    LIMIT 1
                    """,
                    (token_hash,)
                )
                resultado = cursor.fetchone()

                if not resultado:
                    return None

                usuario_id, email, confirmado, expira_em = resultado

                # Verificar se já foi confirmado
                if confirmado:
                    return None

                # Verificar se expirou
                if isinstance(expira_em, str):
                    expira_em = datetime.fromisoformat(expira_em.replace("Z", "+00:00"))
                
                if agora > expira_em:
                    return None

                return {
                    "id_usuario": usuario_id,
                    "email": email,
                    "token_hash": token_hash
                }

            except Exception as e:
                print(f"Erro ao verificar token: {e}")
                return None

    def marcar_como_confirmado(self, token_hash: str) -> bool:
        """
        Marca um token como confirmado (email verificado).
        
        Args:
            token_hash: Hash do token confirmado
        
        Returns:
            True se marcado com sucesso
        """
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE confirmacao_email SET confirmado = %s WHERE token_hash = %s",
                    (True, token_hash)
                )
            return True
        except Exception as e:
            print(f"Erro ao marcar email como confirmado: {e}")
            return False
