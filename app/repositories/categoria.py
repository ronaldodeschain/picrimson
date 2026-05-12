from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.categoria import Categoria, CategoriaCriarAtualizar

class CategoriaRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_categorias(self) -> list[Categoria]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM categorias")
            linhas = cursor.fetchall()
            return [
                Categoria(
                    id_categoria=linha[0],
                    nome_categoria=linha[1]
                ) for linha in linhas
            ]

    async def get_categoria(self, categoria_id: int) -> Categoria | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM categorias WHERE id_categoria = %s",
                (categoria_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Categoria(
                    id_categoria=linha[0],
                    nome_categoria=linha[1]
                )
            return None

    async def criar_categoria(self,
                              categoria: CategoriaCriarAtualizar) -> Categoria | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO categorias(nome_categoria) VALUES (%s) RETURNING id_categoria",
                (categoria.nome_categoria,)
            )
            id_categoria = cursor.fetchone()[0]
            return Categoria(
                id_categoria=id_categoria,
                nome_categoria=categoria.nome_categoria
            )

    async def update_categoria(self, categoria_id: int,
                               categoria: CategoriaCriarAtualizar) -> Categoria | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE categorias SET nome_categoria = %s WHERE id_categoria = %s",
                (categoria.nome_categoria, categoria_id)
            )
            if cursor.rowcount == 0:
                return None
            return Categoria(
                id_categoria=categoria_id,
                nome_categoria=categoria.nome_categoria
            )

    async def delete_categoria(self, categoria_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM categorias WHERE id_categoria = %s",
                (categoria_id,)
            )
            return cursor.rowcount > 0