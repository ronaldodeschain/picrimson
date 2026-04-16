from typing import cast
from app.database.local import Database
from app.models.item_pedido import ItemPedido, ItemPedidoCriarAtualizar


class ItemPedidoRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_itens_pedido(self) -> list[ItemPedido]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM item_pedidos")
            linhas = cursor.fetchall()
            return [
                ItemPedido(
                    id_item_pedido=linha[0],
                    id_usuario=linha[1],
                    id_produto=linha[2],
                    id_carrinho=linha[3]
                ) for linha in linhas
            ]

    async def get_item_pedido(self, item_id: int) -> ItemPedido | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM item_pedidos WHERE id_item_pedido = ?",
                (item_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return ItemPedido(
                    id_item_pedido=linha[0],
                    id_usuario=linha[1],
                    id_produto=linha[2],
                    id_carrinho=linha[3]
                )
            return None

    async def criar_item_pedido(self, item: ItemPedidoCriarAtualizar) -> ItemPedido:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO item_pedidos (id_usuario, id_produto, id_carrinho) VALUES (?, ?, ?)",
                (item.id_usuario, item.id_produto, item.id_carrinho)
            )
            id_item_pedido = cast(int, cursor.lastrowid)
            return ItemPedido(
                id_item_pedido=id_item_pedido,
                id_usuario=item.id_usuario,
                id_produto=item.id_produto,
                id_carrinho=item.id_carrinho
            )  # type: ignore

    async def update_item_pedido(self, item_id: int, item: ItemPedidoCriarAtualizar) -> ItemPedido | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE itens_pedido SET id_usuario = ?, id_produto = ?, id_carrinho = ? WHERE id_item_pedido = ?",
                (item.id_usuario, item.id_produto, item.id_carrinho, item_id)
            )
            if cursor.rowcount > 0:
                return ItemPedido(
                    id_item_pedido=item_id,
                    id_usuario=item.id_usuario,
                    id_produto=item.id_produto,
                    id_carrinho=item.id_carrinho
                )
            return None

    async def delete_item_pedido(self, item_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("DELETE FROM itens_pedido WHERE id_item_pedido = ?", (item_id,))
            return cursor.rowcount > 0