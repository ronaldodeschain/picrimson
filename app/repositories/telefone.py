from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.telefone import Telefone, TelefoneCriarAtualizar


class TelefoneRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_telefones(self) -> list[Telefone]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM telefone")
            linhas = cursor.fetchall()
            return [
                Telefone(
                    id_telefone=linha[0],
                    telefone_principal=linha[1],
                    telefone_secundario=linha[2],
                    id_usuario=linha[3]
                ) for linha in linhas
            ]

    async def get_telefone(self, telefone_id: int) -> Telefone | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM telefone WHERE id_telefone = %s",
                (telefone_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Telefone(
                    id_telefone=linha[0],
                    telefone_principal=linha[1],
                    telefone_secundario=linha[2],
                    id_usuario=linha[3]
                )
            return None

    async def criar_telefone(self,
                              telefone: TelefoneCriarAtualizar) -> Telefone | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO telefone(telefone_principal, telefone_secundario, id_usuario) VALUES (%s, %s, %s) RETURNING id_telefone",
                (telefone.telefone_principal, telefone.telefone_secundario, telefone.id_usuario)
            )
            id_telefone = cursor.fetchone()[0]
            return Telefone(
                id_telefone=id_telefone,
                telefone_principal=telefone.telefone_principal,
                telefone_secundario=telefone.telefone_secundario,
                id_usuario=telefone.id_usuario
            )

    async def update_telefone(self, telefone_id: int,
                              telefone: TelefoneCriarAtualizar) -> Telefone | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE telefone SET telefone_principal = %s, telefone_secundario = %s, id_usuario = %s WHERE id_telefone = %s",
                (telefone.telefone_principal, telefone.telefone_secundario, telefone.id_usuario, telefone_id)
            )
            if cursor.rowcount == 0:
                return None
            return Telefone(
                id_telefone=telefone_id,
                telefone_principal=telefone.telefone_principal,
                telefone_secundario=telefone.telefone_secundario,
                id_usuario=telefone.id_usuario
            )

    async def delete_telefone(self, telefone_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM telefone WHERE id_telefone = %s",
                (telefone_id,)
            )
            return cursor.rowcount > 0