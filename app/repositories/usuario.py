from typing import cast
from app.database.local import Database
from app.models.usuario import Usuario,UsuarioCriarAtualizar


class UsuarioRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_usuarios(self) -> list[Usuario]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM usuarios")
            linhas = cursor.fetchall()
            return [
                Usuario(
                    id_usuario=linha[0],
                    nome_usuario=linha[1],
                    login=linha[2],
                    senha=linha[3],
                    cpf=linha[4]
                    , role=linha[5] if len(linha) > 5 else "user"
                ) for linha in linhas
            ]
    
    async def get_cliente(self,usuario_id:int) -> Usuario |None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM usuarios WHERE id_usuario =?",
                (usuario_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Usuario(
                    id_usuario=linha[0],
                    nome_usuario=linha[1],
                    login=linha[2],
                    senha=linha[3],
                    cpf=linha[4]
                        , role=linha[5] if len(linha) > 5 else "user"
                )
            return None
            
    async def get_usuario_por_email_e_senha(self,
                                            email: str,
                                            senha: str) -> Usuario | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
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
                        , role=linha[5] if len(linha) > 5 else "user"
                )


    async def get_usuario_por_email(self, email: str) -> Usuario | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
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
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO usuarios(nome_usuario,login,senha,cpf,role) values(?,?,?,?,?)",
                (usuario.nome_usuario,usuario.login,usuario.senha,usuario.cpf, usuario.role)
            )
            id_user = cast(int, cursor.lastrowid)
            return Usuario(
                id_usuario=id_user,
                nome_usuario=usuario.nome_usuario,
                login=usuario.login,
                senha=usuario.senha,
                cpf=usuario.cpf,
                role=usuario.role
            )
    
    async def update_usuario(self,usario_id:int,
                            usuario:UsuarioCriarAtualizar) -> Usuario | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE usuarios SET nome_usuario=?, login=?, senha=?, cpf=?, role=? WHERE id_usuario=?",
                (usuario.nome_usuario,usuario.login,usuario.senha,usuario.cpf, usuario.role, usario_id)
            )  
            if cursor.rowcount == 0:
                return None
            return Usuario(
                nome_usuario=usuario.nome_usuario,
                login=usuario.login,
                senha=usuario.senha,
                cpf=usuario.cpf
                , role=usuario.role
            )

    async def delete_usuario(self,usuario_int:int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM usuarios WHERE id_usuario=?",
                (usuario_int,)
            )
            return cursor.rowcount > 0