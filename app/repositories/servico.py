from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.servico import Servico, ServicoCriarAtualizar


class ServicoRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_servicos(self) -> list[Servico]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM servico")
            linhas = cursor.fetchall()
            return [
                Servico(
                    id_servico=linha[0],
                    tipo_servico=linha[1],
                    valor_servico=linha[2],
                    descricao=linha[3],
                    id_pedido=linha[4],
                    id_orcamento=linha[5]
                ) for linha in linhas
            ]

    async def get_servico(self, servico_id: int) -> Servico | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM servico WHERE id_servico = %s",
                (servico_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Servico(
                    id_servico=linha[0],
                    tipo_servico=linha[1],
                    valor_servico=linha[2],
                    descricao=linha[3],
                    id_pedido=linha[4],
                    id_orcamento=linha[5]
                )
            return None

    async def criar_servico(self,
                             servico: ServicoCriarAtualizar) -> Servico | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO servico(tipo_servico, valor_servico, descricao, id_pedido, id_orcamento) VALUES (%s, %s, %s, %s, %s) RETURNING id_servico",
                (servico.tipo_servico, servico.valor_servico, servico.descricao, servico.id_pedido, servico.id_orcamento)
            )
            id_servico = cursor.fetchone()[0]
            return Servico(
                id_servico=id_servico,
                tipo_servico=servico.tipo_servico,
                valor_servico=servico.valor_servico,
                descricao=servico.descricao,
                id_pedido=servico.id_pedido,
                id_orcamento=servico.id_orcamento
            )

    async def update_servico(self, servico_id: int,
                             servico: ServicoCriarAtualizar) -> Servico | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE servico SET tipo_servico = %s, valor_servico = %s, descricao = %s, id_pedido = %s, id_orcamento = %s WHERE id_servico = %s",
                (servico.tipo_servico, servico.valor_servico, servico.descricao, servico.id_pedido, servico.id_orcamento, servico_id)
            )
            if cursor.rowcount == 0:
                return None
            return Servico(
                id_servico=servico_id,
                tipo_servico=servico.tipo_servico,
                valor_servico=servico.valor_servico,
                descricao=servico.descricao,
                id_pedido=servico.id_pedido,
                id_orcamento=servico.id_orcamento
            )

    async def delete_servico(self, servico_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM servico WHERE id_servico = %s",
                (servico_id,)
            )
            return cursor.rowcount > 0