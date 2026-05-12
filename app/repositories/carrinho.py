from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.carrinho import Carrinho, CarrinhoCriarAtualizar


class CarrinhoRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_carrinhos(self) -> list[Carrinho]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM carrinho")
            linhas = cursor.fetchall()
            return [
                Carrinho(
                    id_carrinho=linha[0],
                    id_servico=linha[1],
                    id_pedido=linha[2],
                    id_item_pedido=linha[3],
                    id_usuario=linha[4]
                ) for linha in linhas
            ]

    async def get_carrinho(self, carrinho_id: int) -> Carrinho | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM carrinho WHERE id_carrinho = %s",
                (carrinho_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Carrinho(
                    id_carrinho=linha[0],
                    id_servico=linha[1],
                    id_pedido=linha[2],
                    id_item_pedido=linha[3],
                    id_usuario=linha[4]
                )
            return None

    async def criar_carrinho(self,
                              carrinho: CarrinhoCriarAtualizar) -> Carrinho | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO carrinho(id_servico, id_pedido, id_item_pedido, id_usuario) VALUES (%s, %s, %s, %s) RETURNING id_carrinho",
                (carrinho.id_servico, carrinho.id_pedido, carrinho.id_item_pedido, carrinho.id_usuario)
            )
            id_carrinho = cursor.fetchone()[0]
            return Carrinho(
                id_carrinho=id_carrinho,
                id_servico=carrinho.id_servico,
                id_pedido=carrinho.id_pedido,
                id_item_pedido=carrinho.id_item_pedido,
                id_usuario=carrinho.id_usuario
            )

    async def update_carrinho(self, carrinho_id: int,
                              carrinho: CarrinhoCriarAtualizar) -> Carrinho | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE carrinho SET id_servico = %s, id_pedido = %s, id_item_pedido = %s, id_usuario = %s WHERE id_carrinho = %s",
                (carrinho.id_servico, carrinho.id_pedido, carrinho.id_item_pedido, carrinho.id_usuario, carrinho_id)
            )
            if cursor.rowcount == 0:
                return None
            return Carrinho(
                id_carrinho=carrinho_id,
                id_servico=carrinho.id_servico,
                id_pedido=carrinho.id_pedido,
                id_item_pedido=carrinho.id_item_pedido,
                id_usuario=carrinho.id_usuario
            )

    async def delete_carrinho(self, carrinho_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM carrinho WHERE id_carrinho = %s",
                (carrinho_id,)
            )
            return cursor.rowcount > 0