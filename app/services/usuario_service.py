from app.repositories.usuario import UsuarioRepository
from app.repositories.email import EmailRepository
from app.models.usuario import UsuarioCriarAtualizar
from app.models.email import EmailCriarAtualizar
from app.models.endereco import EnderecoCriarAtualizar
from app.models.telefone import TelefoneCriarAtualizar

class UsuarioService:
    def __init__(self, usuario_repo, email_repo, endereco_repo, telefone_repo):
        self.usuario_repo = usuario_repo
        self.email_repo = email_repo
        self.endereco_repo = endereco_repo
        self.telefone_repo = telefone_repo

    async def registrar_usuario(self, nome, email, senha, cpf):
        """Encapsula a lógica de cadastro e validações de e-mail."""
        # 1. Validação de email existente
        email_existente = await self.email_repo.get_email_por_valor(email)
        if email_existente:
            return None, "Este e-mail já está cadastrado no sistema."

        # 2. Criar Usuário
        novo_usuario = UsuarioCriarAtualizar(
            nome_usuario=nome, login=email, senha=senha, cpf=cpf, role="user"
        )
        usuario = await self.usuario_repo.criar_usuario(novo_usuario)
        
        if not usuario or not usuario.id_usuario:
            return None, "Erro ao processar o cadastro do usuário."
            
        uid = usuario.id_usuario

        # 3. Criar entrada na tabela de emails para login
        try:
            await self.email_repo.criar_email(EmailCriarAtualizar(email=email, id_usuario=uid))
        except Exception:
            pass

        # 4. Criar registros base de Endereço e Telefone (Setup Inicial)
        try:
            await self.endereco_repo.criar_endereco(EnderecoCriarAtualizar(
                rua="", numero=0, complemento="", cep="", cidade="", estado="", 
                observacoes="", id_usuario=uid
            ))
        except Exception:
            pass

        try:
            await self.telefone_repo.criar_telefone(TelefoneCriarAtualizar(
                telefone_principal=0, telefone_secundario=0, id_usuario=uid
            ))
        except Exception:
            pass

        return usuario, None