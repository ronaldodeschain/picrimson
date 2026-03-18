from typing import cast
from app.database.local import Database
from app.models.telefone import Telefone, TelefoneCriarAtualizar


class TelefoneRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_telefones(self) -> list[Telefone]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM telefones")
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
                "SELECT * FROM telefones WHERE id_telefone = ?",
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
                "INSERT INTO telefones(telefone_principal, telefone_secundario, id_usuario) VALUES (?, ?, ?)",
                (telefone.telefone_principal, telefone.telefone_secundario, telefone.id_usuario)
            )
            id_telefone = cast(int, cursor.lastrowid)
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
                "UPDATE telefones SET telefone_principal = ?, telefone_secundario = ?, id_usuario = ? WHERE id_telefone = ?",
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
                "DELETE FROM telefones WHERE id_telefone = ?",
                (telefone_id,)
            )
            return cursor.rowcount > 0