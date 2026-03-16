from app.models.usuario import Usuario
from app.repositories.base import BaseRepository

class UsuarioRepository(BaseRepository):
    
    def criar_usuario(self, usuario: Usuario):
        query = """
            INSERT INTO usuarios (nome_usuario, login, senha, cpf)
            VALUES (?, ?, ?, ?)
        """
        # O Context Manager do connect() no local.py já faz o commit ou rollback
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (
                usuario.nome_usuario, 
                usuario.login, 
                usuario.senha, 
                usuario.cpf
            ))
            # Retorna o ID do usuário criado
            return cursor.lastrowid

    def listar_usuarios(self):
        query = "SELECT id_usuario, nome_usuario, login, senha, cpf FROM usuarios"
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Converte as tuplas do banco em objetos Pydantic
            usuarios = []
            for row in rows:
                usuarios.append(Usuario(
                    id_usuario=row[0], nome_usuario=row[1], login=row[2], 
                    senha=row[3], cpf=row[4]
                ))
            return usuarios
