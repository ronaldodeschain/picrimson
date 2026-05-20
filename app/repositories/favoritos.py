from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.favoritos import Favoritos, FavoritosCriarAtualizar


class FavoritosRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_favoritos(self) -> list[Favoritos]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM favoritos")
            linhas = cursor.fetchall()
            return [
                Favoritos(
                    id_favoritos=linha[0],
                    id_produto=linha[1],
                    id_usuario=linha[2]
                ) for linha in linhas
            ]

    async def get_favorito(self, favorito_id: int) -> Favoritos | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM favoritos WHERE id_favoritos = %s",
                (favorito_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Favoritos(
                    id_favoritos=linha[0],
                    id_produto=linha[1],
                    id_usuario=linha[2]
                )
            return None

    async def listar_favoritos_por_usuario(self, id_usuario: int) -> list[Favoritos]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM favoritos WHERE id_usuario = %s",
                (id_usuario,)
            )
            linhas = cursor.fetchall()
            return [
                Favoritos(
                    id_favoritos=linha[0],
                    id_produto=linha[1],
                    id_usuario=linha[2]
                ) for linha in linhas
            ]

    async def criar_favorito(self, favorito: FavoritosCriarAtualizar) -> Favoritos:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO favoritos (id_produto, id_usuario) VALUES (%s, %s) RETURNING id_favoritos",
                (favorito.id_produto, favorito.id_usuario)
            )
            id_favoritos = cursor.fetchone()[0]
            return Favoritos(
                id_favoritos=id_favoritos,
                id_produto=favorito.id_produto,
                id_usuario=favorito.id_usuario
            )

    async def update_favorito(self, favorito_id: int, favorito: FavoritosCriarAtualizar) -> Favoritos | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE favoritos SET id_produto = %s, id_usuario = %s WHERE id_favoritos = %s",
                (favorito.id_produto, favorito.id_usuario, favorito_id)
            )
            if cursor.rowcount > 0:
                return Favoritos(
                    id_favoritos=favorito_id,
                    id_produto=favorito.id_produto,
                    id_usuario=favorito.id_usuario
                )
            return None

    async def delete_favorito(self, favorito_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("DELETE FROM favoritos WHERE id_favoritos = %s", (favorito_id,))
            return cursor.rowcount > 0