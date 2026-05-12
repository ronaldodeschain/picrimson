from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.mensagem import Mensagem, MensagemCriarAtualizar


class MensagemRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_mensagens(self) -> list[Mensagem]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM mensagem")
            linhas = cursor.fetchall()
            return [
                Mensagem(
                    id_mensagem=linha[0],
                    mensagem=linha[1],
                    tipo_mensagem=linha[2],
                    id_pedido=linha[3],
                    id_email=linha[4],
                    id_orcamento=linha[5],
                    id_usuario=linha[6],
                    id_nota_fiscal=linha[7],
                    id_rastreio=linha[8]
                ) for linha in linhas
            ]

    async def get_mensagem(self, mensagem_id: int) -> Mensagem | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM mensagem WHERE id_mensagem = %s",
                (mensagem_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Mensagem(
                    id_mensagem=linha[0],
                    mensagem=linha[1],
                    tipo_mensagem=linha[2],
                    id_pedido=linha[3],
                    id_email=linha[4],
                    id_orcamento=linha[5],
                    id_usuario=linha[6],
                    id_nota_fiscal=linha[7],
                    id_rastreio=linha[8]
                )
            return None

    async def criar_mensagem(self, mensagem: MensagemCriarAtualizar) -> Mensagem:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO mensagem (mensagem, tipo_mensagem, id_pedido, id_email, id_orcamento, id_usuario, id_nota_fiscal, id_rastreio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_mensagem",
                (mensagem.mensagem, mensagem.tipo_mensagem, mensagem.id_pedido, mensagem.id_email, mensagem.id_orcamento, mensagem.id_usuario, mensagem.id_nota_fiscal, mensagem.id_rastreio)
            )
            id_mensagem = cursor.fetchone()[0]
            return Mensagem(
                id_mensagem=id_mensagem,
                mensagem=mensagem.mensagem,
                tipo_mensagem=mensagem.tipo_mensagem,
                id_pedido=mensagem.id_pedido,
                id_email=mensagem.id_email,
                id_orcamento=mensagem.id_orcamento,
                id_usuario=mensagem.id_usuario,
                id_nota_fiscal=mensagem.id_nota_fiscal,
                id_rastreio=mensagem.id_rastreio
            )  # type: ignore

    async def update_mensagem(self, mensagem_id: int, mensagem: MensagemCriarAtualizar) -> Mensagem | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE mensagem SET mensagem = %s, tipo_mensagem = %s, id_pedido = %s, id_email = %s, id_orcamento = %s, id_usuario = %s, id_nota_fiscal = %s, id_rastreio = %s WHERE id_mensagem = %s",
                (mensagem.mensagem, mensagem.tipo_mensagem, mensagem.id_pedido, mensagem.id_email, mensagem.id_orcamento, mensagem.id_usuario, mensagem.id_nota_fiscal, mensagem.id_rastreio, mensagem_id)
            )
            if cursor.rowcount > 0:
                return Mensagem(
                    id_mensagem=mensagem_id,
                    mensagem=mensagem.mensagem,
                    tipo_mensagem=mensagem.tipo_mensagem,
                    id_pedido=mensagem.id_pedido,
                    id_email=mensagem.id_email,
                    id_orcamento=mensagem.id_orcamento,
                    id_usuario=mensagem.id_usuario,
                    id_nota_fiscal=mensagem.id_nota_fiscal,
                    id_rastreio=mensagem.id_rastreio
                )
            return None

    async def delete_mensagem(self, mensagem_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("DELETE FROM mensagem WHERE id_mensagem = %s", (mensagem_id,))
            return cursor.rowcount > 0