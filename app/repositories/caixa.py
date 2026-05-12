from datetime import date
from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.caixa import Caixa, CaixaCriarAtualizar


class CaixaRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_caixas(self) -> list[Caixa]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM caixa")
            linhas = cursor.fetchall()
            return [
                Caixa(
                    id_caixa=linha[0],
                    tipo_movimentacao=linha[1],
                    valor=linha[2],
                    descricao=linha[3],
                    data_movimentacao=date.fromisoformat(linha[4]) if linha[4] else None,
                    id_nota_fiscal=linha[5],
                    id_pagamento=linha[6]
                ) for linha in linhas
            ]

    async def get_caixa(self, caixa_id: int) -> Caixa | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM caixa WHERE id_caixa = %s",
                (caixa_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Caixa(
                    id_caixa=linha[0],
                    tipo_movimentacao=linha[1],
                    valor=linha[2],
                    descricao=linha[3],
                    data_movimentacao=date.fromisoformat(linha[4]) if linha[4] else None,
                    id_nota_fiscal=linha[5],
                    id_pagamento=linha[6]
                )
            return None

    async def criar_caixa(self,
                          caixa: CaixaCriarAtualizar) -> Caixa | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO caixa(tipo_movimentacao, valor, descricao, data_movimentacao, id_nota_fiscal, id_pagamento) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_caixa",
                (caixa.tipo_movimentacao, caixa.valor, caixa.descricao, caixa.data_movimentacao.isoformat() if caixa.data_movimentacao else None, caixa.id_nota_fiscal, caixa.id_pagamento)
            )
            id_caixa = cursor.fetchone()[0]
            return Caixa(
                id_caixa=id_caixa,
                tipo_movimentacao=caixa.tipo_movimentacao,
                valor=caixa.valor,
                descricao=caixa.descricao,
                data_movimentacao=caixa.data_movimentacao,
                id_nota_fiscal=caixa.id_nota_fiscal,
                id_pagamento=caixa.id_pagamento
            )

    async def update_caixa(self, caixa_id: int,
                           caixa: CaixaCriarAtualizar) -> Caixa | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE caixa SET tipo_movimentacao = %s, valor = %s, descricao = %s, data_movimentacao = %s, id_nota_fiscal = %s, id_pagamento = %s WHERE id_caixa = %s",
                (caixa.tipo_movimentacao, caixa.valor, caixa.descricao, caixa.data_movimentacao.isoformat() if caixa.data_movimentacao else None, caixa.id_nota_fiscal, caixa.id_pagamento, caixa_id)
            )
            if cursor.rowcount == 0:
                return None
            return Caixa(
                id_caixa=caixa_id,
                tipo_movimentacao=caixa.tipo_movimentacao,
                valor=caixa.valor,
                descricao=caixa.descricao,
                data_movimentacao=caixa.data_movimentacao,
                id_nota_fiscal=caixa.id_nota_fiscal,
                id_pagamento=caixa.id_pagamento
            )

    async def delete_caixa(self, caixa_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM caixa WHERE id_caixa = %s",
                (caixa_id,)
            )
            return cursor.rowcount > 0