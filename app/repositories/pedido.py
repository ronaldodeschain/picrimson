from typing import cast
from app.database.local import Database
from app.models.pedido import Pedido, PedidoCriarAtualizar


class PedidoRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_pedidos(self) -> list[Pedido]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM pedidos")
            linhas = cursor.fetchall()
            return [
                Pedido(
                    id_pedido=linha[0],
                    valor_total=linha[1],
                    observacoes=linha[2],
                    id_pagamento=linha[3],
                    id_carrinho=linha[4],
                    id_cupom=linha[5],
                    id_servico=linha[6]
                ) for linha in linhas
            ]

    async def get_pedido(self, pedido_id: int) -> Pedido | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM pedidos WHERE id_pedido = ?",
                (pedido_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Pedido(
                    id_pedido=linha[0],
                    valor_total=linha[1],
                    observacoes=linha[2],
                    id_pagamento=linha[3],
                    id_carrinho=linha[4],
                    id_cupom=linha[5],
                    id_servico=linha[6]
                )
            return None

    async def criar_pedido(self,
                           pedido: PedidoCriarAtualizar) -> Pedido | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO pedidos(valor_total, observacoes, id_pagamento, id_carrinho, id_cupom, id_servico) VALUES (?, ?, ?, ?, ?, ?)",
                (pedido.valor_total, pedido.observacoes, pedido.id_pagamento, pedido.id_carrinho, pedido.id_cupom, pedido.id_servico)
            )
            id_pedido = cast(int, cursor.lastrowid)
            return Pedido(
                id_pedido=id_pedido,
                valor_total=pedido.valor_total,
                observacoes=pedido.observacoes,
                id_pagamento=pedido.id_pagamento,
                id_carrinho=pedido.id_carrinho,
                id_cupom=pedido.id_cupom,
                id_servico=pedido.id_servico
            )

    async def update_pedido(self, pedido_id: int,
                            pedido: PedidoCriarAtualizar) -> Pedido | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE pedidos SET valor_total = ?, observacoes = ?, id_pagamento = ?, id_carrinho = ?, id_cupom = ?, id_servico = ? WHERE id_pedido = ?",
                (pedido.valor_total, pedido.observacoes, pedido.id_pagamento, pedido.id_carrinho, pedido.id_cupom, pedido.id_servico, pedido_id)
            )
            if cursor.rowcount == 0:
                return None
            return Pedido(
                id_pedido=pedido_id,
                valor_total=pedido.valor_total,
                observacoes=pedido.observacoes,
                id_pagamento=pedido.id_pagamento,
                id_carrinho=pedido.id_carrinho,
                id_cupom=pedido.id_cupom,
                id_servico=pedido.id_servico
            )

    async def delete_pedido(self, pedido_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM pedidos WHERE id_pedido = ?",
                (pedido_id,)
            )
            return cursor.rowcount > 0