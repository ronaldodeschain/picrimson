from typing import cast
from app.database.local import Database
from app.models.resposta import Resposta, RespostaCriarAtualizar


class RespostaRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_respostas(self) -> list[Resposta]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM resposta")
            linhas = cursor.fetchall()
            return [
                Resposta(
                    id_resposta=linha[0],
                    texto_resposta=linha[1],
                    data_resposta=linha[2],
                    id_usuario=linha[3],
                    id_produto=linha[4]
                ) for linha in linhas
            ]

    async def get_resposta(self, resposta_id: int) -> Resposta | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM resposta WHERE id_resposta = ?",
                (resposta_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Resposta(
                    id_resposta=linha[0],
                    texto_resposta=linha[1],
                    data_resposta=linha[2],
                    id_usuario=linha[3],
                    id_produto=linha[4]
                )
            return None

    async def criar_resposta(self,
                              resposta: RespostaCriarAtualizar) -> Resposta | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO resposta(texto_resposta, data_resposta, id_usuario, id_produto) VALUES (?, ?, ?, ?)",
                (resposta.texto_resposta, resposta.data_resposta, resposta.id_usuario, resposta.id_produto)
            )
            id_resposta = cast(int, cursor.lastrowid)
            return Resposta(
                id_resposta=id_resposta,
                texto_resposta=resposta.texto_resposta,
                data_resposta=resposta.data_resposta,
                id_usuario=resposta.id_usuario,
                id_produto=resposta.id_produto
            )

    async def update_resposta(self, resposta_id: int,
                              resposta: RespostaCriarAtualizar) -> Resposta | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE resposta SET texto_resposta = ?, data_resposta = ?, id_usuario = ?, id_produto = ? WHERE id_resposta = ?",
                (resposta.texto_resposta, resposta.data_resposta, resposta.id_usuario, resposta.id_produto, resposta_id)
            )
            if cursor.rowcount == 0:
                return None
            return Resposta(
                id_resposta=resposta_id,
                texto_resposta=resposta.texto_resposta,
                data_resposta=resposta.data_resposta,
                id_usuario=resposta.id_usuario,
                id_produto=resposta.id_produto
            )

    async def delete_resposta(self, resposta_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM resposta WHERE id_resposta = ?",
                (resposta_id,)
            )
            return cursor.rowcount > 0
