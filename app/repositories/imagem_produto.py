from typing import cast
from app.database.local import Database
from app.models.imagem_produto import ImagemProduto, ImagemProdutoCriarAtualizar


class ImagemProdutoRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_imagens_produto(self) -> list[ImagemProduto]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM imagens_produto")
            linhas = cursor.fetchall()
            return [
                ImagemProduto(
                    id_imagem_produto=linha[0],
                    nome_imagem=linha[1],
                    arquivo_imagem=linha[2],
                    id_produto=linha[3]
                ) for linha in linhas
            ]

    async def get_imagem_produto(self, imagem_id: int) -> ImagemProduto | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM imagens_produto WHERE id_imagem_produto = ?",
                (imagem_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return ImagemProduto(
                    id_imagem_produto=linha[0],
                    nome_imagem=linha[1],
                    arquivo_imagem=linha[2],
                    id_produto=linha[3]
                )
            return None

    async def criar_imagem_produto(self, imagem: ImagemProdutoCriarAtualizar) -> ImagemProduto:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO imagens_produto (nome_imagem, arquivo_imagem, id_produto) VALUES (?, ?, ?)",
                (imagem.nome_imagem, imagem.arquivo_imagem, imagem.id_produto)
            )
            id_imagem_produto = cast(int, cursor.lastrowid)
            return ImagemProduto(
                id_imagem_produto=id_imagem_produto,
                nome_imagem=imagem.nome_imagem,
                arquivo_imagem=imagem.arquivo_imagem,
                id_produto=imagem.id_produto
            )

    async def update_imagem_produto(self, imagem_id: int, imagem: ImagemProdutoCriarAtualizar) -> ImagemProduto | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE imagens_produto SET nome_imagem = ?, arquivo_imagem = ?, id_produto = ? WHERE id_imagem_produto = ?",
                (imagem.nome_imagem, imagem.arquivo_imagem, imagem.id_produto, imagem_id)
            )
            if cursor.rowcount > 0:
                return ImagemProduto(
                    id_imagem_produto=imagem_id,
                    nome_imagem=imagem.nome_imagem,
                    arquivo_imagem=imagem.arquivo_imagem,
                    id_produto=imagem.id_produto
                )
            return None

    async def delete_imagem_produto(self, imagem_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("DELETE FROM imagens_produto WHERE id_imagem_produto = ?", (imagem_id,))
            return cursor.rowcount > 0