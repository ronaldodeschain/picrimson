from typing import cast
from app.database.local import Database
from app.models.rastreio import Rastreio, RastreioCriarAtualizar


class RastreioRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_rastreios(self) -> list[Rastreio]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM rastreios")
            linhas = cursor.fetchall()
            return [
                Rastreio(
                    id_rastreio=linha[0],
                    codigo_rastreio=linha[1],
                    id_entrega=linha[2],
                    id_mensagem=linha[3]
                ) for linha in linhas
            ]

    async def get_rastreio(self, rastreio_id: int) -> Rastreio | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM rastreios WHERE id_rastreio = ?",
                (rastreio_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Rastreio(
                    id_rastreio=linha[0],
                    codigo_rastreio=linha[1],
                    id_entrega=linha[2],
                    id_mensagem=linha[3]
                )
            return None

    async def criar_rastreio(self, rastreio: RastreioCriarAtualizar) -> Rastreio:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO rastreios (codigo_rastreio, id_entrega, id_mensagem) VALUES (?, ?, ?)",
                (rastreio.codigo_rastreio, rastreio.id_entrega, rastreio.id_mensagem)
            )
            id_rastreio = cast(int, cursor.lastrowid)
            return Rastreio(
                id_rastreio=id_rastreio,
                codigo_rastreio=rastreio.codigo_rastreio,
                id_entrega=rastreio.id_entrega,
                id_mensagem=rastreio.id_mensagem
            )  # type: ignore

    async def update_rastreio(self, rastreio_id: int, rastreio: RastreioCriarAtualizar) -> Rastreio | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE rastreios SET codigo_rastreio = ?, id_entrega = ?, id_mensagem = ? WHERE id_rastreio = ?",
                (rastreio.codigo_rastreio, rastreio.id_entrega, rastreio.id_mensagem, rastreio_id)
            )
            if cursor.rowcount > 0:
                return Rastreio(
                    id_rastreio=rastreio_id,
                    codigo_rastreio=rastreio.codigo_rastreio,
                    id_entrega=rastreio.id_entrega,
                    id_mensagem=rastreio.id_mensagem
                )
            return None

    async def delete_rastreio(self, rastreio_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("DELETE FROM rastreios WHERE id_rastreio = ?", (rastreio_id,))
            return cursor.rowcount > 0