from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.pergunta import Pergunta, PerguntaCriarAtualizar


class PerguntaRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_perguntas(self) -> list[Pergunta]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM pergunta")
            linhas = cursor.fetchall()
            return [
                Pergunta(
                    id_pergunta=linha[0],
                    pergunta=linha[1],
                    data_criacao=linha[2],
                    id_usuario=linha[3],
                    id_produto=linha[4],
                    id_resposta=linha[5]
                ) for linha in linhas
            ]

    async def get_pergunta(self, pergunta_id: int) -> Pergunta | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM pergunta WHERE id_pergunta = %s",
                (pergunta_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Pergunta(
                    id_pergunta=linha[0],
                    pergunta=linha[1],
                    data_criacao=linha[2],
                    id_usuario=linha[3],
                    id_produto=linha[4],
                    id_resposta=linha[5]
                )
            return None

    async def criar_pergunta(self,
                              pergunta: PerguntaCriarAtualizar) -> Pergunta | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO pergunta(pergunta, data_criacao, id_usuario, id_produto, id_resposta) VALUES (%s, %s, %s, %s, %s) RETURNING id_pergunta",
                (pergunta.pergunta, pergunta.data_criacao, pergunta.id_usuario, pergunta.id_produto, pergunta.id_resposta)
            )
            id_pergunta = cursor.fetchone()[0]
            return Pergunta(
                id_pergunta=id_pergunta,
                pergunta=pergunta.pergunta,
                data_criacao=pergunta.data_criacao,
                id_usuario=pergunta.id_usuario,
                id_produto=pergunta.id_produto,
                id_resposta=pergunta.id_resposta
            )

    async def update_pergunta(self, pergunta_id: int,
                              pergunta: PerguntaCriarAtualizar) -> Pergunta | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE pergunta SET pergunta = %s, data_criacao = %s, id_usuario = %s, id_produto = %s, id_resposta = %s WHERE id_pergunta = %s",
                (pergunta.pergunta, pergunta.data_criacao, pergunta.id_usuario, pergunta.id_produto, pergunta.id_resposta, pergunta_id)
            )
            if cursor.rowcount == 0:
                return None
            return Pergunta(
                id_pergunta=pergunta_id,
                pergunta=pergunta.pergunta,
                data_criacao=pergunta.data_criacao,
                id_usuario=pergunta.id_usuario,
                id_produto=pergunta.id_produto,
                id_resposta=pergunta.id_resposta
            )

    async def delete_pergunta(self, pergunta_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM pergunta WHERE id_pergunta = %s",
                (pergunta_id,)
            )
            return cursor.rowcount > 0
