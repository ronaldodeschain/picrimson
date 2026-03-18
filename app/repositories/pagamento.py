from datetime import datetime, date
from typing import cast
from app.database.local import Database
from app.models.pagamento import Pagamento, PagamentoCriarAtualizar


class PagamentoRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_pagamentos(self) -> list[Pagamento]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM pagamentos")
            linhas = cursor.fetchall()
            return [
                Pagamento(
                    id_pagamento=linha[0],
                    expiracao=datetime.fromisoformat(linha[1]) if linha[1] else None,
                    valor_total=linha[2],
                    data_pagamento=date.fromisoformat(linha[3]) if linha[3] else None,
                    pixTxid=linha[4],
                    id_pedido=linha[5],
                    id_caixa=linha[6],
                    id_nota_fiscal=linha[7],
                    id_entrega=linha[8]
                ) for linha in linhas
            ]

    async def get_pagamento(self, pagamento_id: int) -> Pagamento | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM pagamentos WHERE id_pagamento = ?",
                (pagamento_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Pagamento(
                    id_pagamento=linha[0],
                    expiracao=datetime.fromisoformat(linha[1]) if linha[1] else None,
                    valor_total=linha[2],
                    data_pagamento=date.fromisoformat(linha[3]) if linha[3] else None,
                    pixTxid=linha[4],
                    id_pedido=linha[5],
                    id_caixa=linha[6],
                    id_nota_fiscal=linha[7],
                    id_entrega=linha[8]
                )
            return None

    async def criar_pagamento(self,
                              pagamento: PagamentoCriarAtualizar) -> Pagamento | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO pagamentos(expiracao, valor_total, data_pagamento, pixTxid, id_pedido, id_caixa, id_nota_fiscal, id_entrega) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (pagamento.expiracao.isoformat() if pagamento.expiracao else None, pagamento.valor_total, pagamento.data_pagamento.isoformat() if pagamento.data_pagamento else None, pagamento.pixTxid, pagamento.id_pedido, pagamento.id_caixa, pagamento.id_nota_fiscal, pagamento.id_entrega)
            )
            id_pagamento = cast(int, cursor.lastrowid)
            return Pagamento(
                id_pagamento=id_pagamento,
                expiracao=pagamento.expiracao,
                valor_total=pagamento.valor_total,
                data_pagamento=pagamento.data_pagamento,
                pixTxid=pagamento.pixTxid,
                id_pedido=pagamento.id_pedido,
                id_caixa=pagamento.id_caixa,
                id_nota_fiscal=pagamento.id_nota_fiscal,
                id_entrega=pagamento.id_entrega
            )

    async def update_pagamento(self, pagamento_id: int,
                               pagamento: PagamentoCriarAtualizar) -> Pagamento | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE pagamentos SET expiracao = ?, valor_total = ?, data_pagamento = ?, pixTxid = ?, id_pedido = ?, id_caixa = ?, id_nota_fiscal = ?, id_entrega = ? WHERE id_pagamento = ?",
                (pagamento.expiracao.isoformat() if pagamento.expiracao else None, pagamento.valor_total, pagamento.data_pagamento.isoformat() if pagamento.data_pagamento else None, pagamento.pixTxid, pagamento.id_pedido, pagamento.id_caixa, pagamento.id_nota_fiscal, pagamento.id_entrega, pagamento_id)
            )
            if cursor.rowcount == 0:
                return None
            return Pagamento(
                id_pagamento=pagamento_id,
                expiracao=pagamento.expiracao,
                valor_total=pagamento.valor_total,
                data_pagamento=pagamento.data_pagamento,
                pixTxid=pagamento.pixTxid,
                id_pedido=pagamento.id_pedido,
                id_caixa=pagamento.id_caixa,
                id_nota_fiscal=pagamento.id_nota_fiscal,
                id_entrega=pagamento.id_entrega
            )

    async def delete_pagamento(self, pagamento_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM pagamentos WHERE id_pagamento = ?",
                (pagamento_id,)
            )
            return cursor.rowcount > 0