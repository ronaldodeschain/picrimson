from typing import cast
from app.database.local import Database
from app.models.cupom import Cupom, CupomCriarAtualizar


class CupomRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_cupons(self) -> list[Cupom]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM cupons")
            linhas = cursor.fetchall()
            return [
                Cupom(
                    id_cupom=linha[0],
                    chave_cupom=linha[1],
                    valor_cupom=linha[2],
                    tipo_cupom=linha[3],
                    id_pedido=linha[4]
                ) for linha in linhas
            ]

    async def get_cupom(self, cupom_id: int) -> Cupom | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM cupons WHERE id_cupom = ?",
                (cupom_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Cupom(
                    id_cupom=linha[0],
                    chave_cupom=linha[1],
                    valor_cupom=linha[2],
                    tipo_cupom=linha[3],
                    id_pedido=linha[4]
                )
            return None

    async def criar_cupom(self,
                           cupom: CupomCriarAtualizar) -> Cupom | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO cupons(chave_cupom, valor_cupom, tipo_cupom, id_pedido) VALUES (?, ?, ?, ?)",
                (cupom.chave_cupom, cupom.valor_cupom, cupom.tipo_cupom, cupom.id_pedido)
            )
            id_cupom = cast(int, cursor.lastrowid)
            return Cupom(
                id_cupom=id_cupom,
                chave_cupom=cupom.chave_cupom,
                valor_cupom=cupom.valor_cupom,
                tipo_cupom=cupom.tipo_cupom,
                id_pedido=cupom.id_pedido
            )

    async def update_cupom(self, cupom_id: int,
                           cupom: CupomCriarAtualizar) -> Cupom | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE cupons SET chave_cupom = ?, valor_cupom = ?, tipo_cupom = ?, id_pedido = ? WHERE id_cupom = ?",
                (cupom.chave_cupom, cupom.valor_cupom, cupom.tipo_cupom, cupom.id_pedido, cupom_id)
            )
            if cursor.rowcount == 0:
                return None
            return Cupom(
                id_cupom=cupom_id,
                chave_cupom=cupom.chave_cupom,
                valor_cupom=cupom.valor_cupom,
                tipo_cupom=cupom.tipo_cupom,
                id_pedido=cupom.id_pedido
            )

    async def delete_cupom(self, cupom_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM cupons WHERE id_cupom = ?",
                (cupom_id,)
            )
            return cursor.rowcount > 0