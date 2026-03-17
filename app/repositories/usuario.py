from app.database.local import Database
from app.models.usuario import Usuario,UsuarioCriarAtualizar


class UsuarioRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_usuarios(self) -> list[Usuario]:
        with self.db.connect() as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM usuarios")
            linhas = cursor.fetchall()
            return [
                Usuario(
                    id_usuario=linha[0],
                    nome_usuario=linha[1],
                    login=linha[2],
                    senha=linha[3],
                    cpf=linha[4]
                ) for linha in linhas
            ]
    
    async def get_usuario_por_email_e_senha(self,
                                            email: str,
                                            senha: str) -> Usuario | None:
        with self.db.connect() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM usuarios WHERE email =? AND senha =?",
                (email, senha))
            linha = cursor.fetchone()
            if linha:
                return Usuario(
                    id_usuario=linha[0],
                    nome_usuario=linha[1],
                    login=linha[2],
                    senha=linha[3],
                    cpf=linha[4]
                )


    async def get_usuario_por_email(self, email: str) -> Usuario | None:
        with self.db.connect() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM usuarios WHERE email =?",
                (email))
            linha= cursor.fetchone()
            if linha:
                return Usuario(
                    id_usuario=linha[0],
                    nome_usuario=linha[1],
                    login=linha[2],
                    senha=linha[3],
                    cpf=linha[4])
            return None

    async def criar_usuario(self,
                            usuario: UsuarioCriarAtualizar) -> Usuario|None:
        with self.db.connect() as conexion:
            cursor = conexion.cursor()
            cursor.execute(
                "INSERT INTO usuarios(nome_usuario,login,senha,cpf) values(?,?,?,?)",
                (usuario.nome_usuario,usuario.login,usuario.senha,usuario.cpf)
            )
            id_user = cursor.lastrowid
            return Usuario(
                id_usuario=id_user,
                nome_usuario=usuario.nome_usuario,
                login=usuario.login,
                senha=usuario.senha,
                cpf=usuario.cpf
            )