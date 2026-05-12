from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.item_pedido import ItemPedido, ItemPedidoCriarAtualizar


class ItemPedidoRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
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
                "SELECT * FROM item_pedidos WHERE id_item_pedido = %s",
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
                "INSERT INTO item_pedidos (id_usuario, id_produto, id_carrinho) VALUES (%s, %s, %s) RETURNING id_item_pedido",
                (item.id_usuario, item.id_produto, item.id_carrinho)
            )
            id_item_pedido = cursor.fetchone()[0]
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
                "UPDATE item_pedidos SET id_usuario = %s, id_produto = %s, id_carrinho = %s WHERE id_item_pedido = %s",
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
            cursor.execute("DELETE FROM item_pedidos WHERE id_item_pedido = %s", (item_id,))
            return cursor.rowcount > 0