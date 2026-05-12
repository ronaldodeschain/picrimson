from datetime import date
from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.entrega import Entrega, EntregaCriarAtualizar


class EntregaRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_entregas(self) -> list[Entrega]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM entrega")
            linhas = cursor.fetchall()
            return [
                Entrega(
                    id_entrega=linha[0],
                    mensagem=linha[1],
                    tipo_mensagem=linha[2],
                    data_entrega_prevista=date.fromisoformat(linha[3]),
                    data_envio=date.fromisoformat(linha[4]),
                    tipo_entrega=linha[5],
                    endereco_entrega=linha[6],
                    observacoes=linha[7],
                    data_pedido=date.fromisoformat(linha[8]),
                    status_entrega=linha[9],
                    id_pedido=linha[10],
                    id_rastreio=linha[11]
                ) for linha in linhas
            ]

    async def get_entrega(self, entrega_id: int) -> Entrega | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM entrega WHERE id_entrega = %s",
                (entrega_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Entrega(
                    id_entrega=linha[0],
                    mensagem=linha[1],
                    tipo_mensagem=linha[2],
                    data_entrega_prevista=date.fromisoformat(linha[3]),
                    data_envio=date.fromisoformat(linha[4]),
                    tipo_entrega=linha[5],
                    endereco_entrega=linha[6],
                    observacoes=linha[7],
                    data_pedido=date.fromisoformat(linha[8]),
                    status_entrega=linha[9],
                    id_pedido=linha[10],
                    id_rastreio=linha[11]
                )
            return None

    async def criar_entrega(self, entrega: EntregaCriarAtualizar) -> Entrega:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO entrega (mensagem, tipo_mensagem, data_entrega_prevista, data_envio, tipo_entrega, endereco_entrega, observacoes, data_pedido, status_entrega, id_pedido, id_rastreio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_entrega",
                (entrega.mensagem, entrega.tipo_mensagem, entrega.data_entrega_prevista.isoformat(), entrega.data_envio.isoformat(), entrega.tipo_entrega, entrega.endereco_entrega, entrega.observacoes, entrega.data_pedido.isoformat(), entrega.status_entrega, entrega.id_pedido, entrega.id_rastreio)
            )
            id_entrega = cursor.fetchone()[0]
            return Entrega(
                id_entrega=id_entrega,
                mensagem=entrega.mensagem,
                tipo_mensagem=entrega.tipo_mensagem,
                data_entrega_prevista=entrega.data_entrega_prevista,
                data_envio=entrega.data_envio,
                tipo_entrega=entrega.tipo_entrega,
                endereco_entrega=entrega.endereco_entrega,
                observacoes=entrega.observacoes,
                data_pedido=entrega.data_pedido,
                status_entrega=entrega.status_entrega,
                id_pedido=entrega.id_pedido,
                id_rastreio=entrega.id_rastreio
            )

    async def update_entrega(self, entrega_id: int, entrega: EntregaCriarAtualizar) -> Entrega | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE entrega SET mensagem = %s, tipo_mensagem = %s, data_entrega_prevista = %s, data_envio = %s, tipo_entrega = %s, endereco_entrega = %s, observacoes = %s, data_pedido = %s, status_entrega = %s, id_pedido = %s, id_rastreio = %s WHERE id_entrega = %s",
                (entrega.mensagem, entrega.tipo_mensagem, entrega.data_entrega_prevista.isoformat(), entrega.data_envio.isoformat(), entrega.tipo_entrega, entrega.endereco_entrega, entrega.observacoes, entrega.data_pedido.isoformat(), entrega.status_entrega, entrega.id_pedido, entrega.id_rastreio, entrega_id)
            )
            if cursor.rowcount > 0:
                return Entrega(
                    id_entrega=entrega_id,
                    mensagem=entrega.mensagem,
                    tipo_mensagem=entrega.tipo_mensagem,
                    data_entrega_prevista=entrega.data_entrega_prevista,
                    data_envio=entrega.data_envio,
                    tipo_entrega=entrega.tipo_entrega,
                    endereco_entrega=entrega.endereco_entrega,
                    observacoes=entrega.observacoes,
                    data_pedido=entrega.data_pedido,
                    status_entrega=entrega.status_entrega,
                    id_pedido=entrega.id_pedido,
                    id_rastreio=entrega.id_rastreio
                )
            return None

    async def delete_entrega(self, entrega_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("DELETE FROM entrega WHERE id_entrega = %s", (entrega_id,))
            return cursor.rowcount > 0