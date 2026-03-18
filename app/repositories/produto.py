from typing import cast
from app.database.local import Database
from app.models.produto import Produto, ProdutoCriarAtualizar


class ProdutoRepository:
    def __init__(self, db: Database):
        self.db = db

    async def listar_produtos(self) -> list[Produto]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute("SELECT * FROM produtos")
            linhas = cursor.fetchall()
            return [
                Produto(
                    id_produto=linha[0],
                    nome_produto=linha[1],
                    descricao=linha[2],
                    material=linha[3],
                    altura=linha[4],
                    comprimento=linha[5],
                    largura=linha[6],
                    quantidade=linha[7],
                    peso=linha[8],
                    valor=linha[9]
                ) for linha in linhas
            ]

    async def get_produto(self, produto_id: int) -> Produto | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT * FROM produtos WHERE id_produto = ?",
                (produto_id,)
            )
            linha = cursor.fetchone()
            if linha:
                return Produto(
                    id_produto=linha[0],
                    nome_produto=linha[1],
                    descricao=linha[2],
                    material=linha[3],
                    altura=linha[4],
                    comprimento=linha[5],
                    largura=linha[6],
                    quantidade=linha[7],
                    peso=linha[8],
                    valor=linha[9]
                )
            return None

    async def criar_produto(self,
                             produto: ProdutoCriarAtualizar) -> Produto | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO produtos(nome_produto, descricao, material, altura, comprimento, largura, quantidade, peso, valor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (produto.nome_produto, produto.descricao, produto.material, produto.altura, produto.comprimento, produto.largura, produto.quantidade, produto.peso, produto.valor)
            )
            id_produto = cast(int, cursor.lastrowid)
            return Produto(
                id_produto=id_produto,
                nome_produto=produto.nome_produto,
                descricao=produto.descricao,
                material=produto.material,
                altura=produto.altura,
                comprimento=produto.comprimento,
                largura=produto.largura,
                quantidade=produto.quantidade,
                peso=produto.peso,
                valor=produto.valor
            )

    async def update_produto(self, produto_id: int,
                             produto: ProdutoCriarAtualizar) -> Produto | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE produtos SET nome_produto = ?, descricao = ?, material = ?, altura = ?, comprimento = ?, largura = ?, quantidade = ?, peso = ?, valor = ? WHERE id_produto = ?",
                (produto.nome_produto, produto.descricao, produto.material, produto.altura, produto.comprimento, produto.largura, produto.quantidade, produto.peso, produto.valor, produto_id)
            )
            if cursor.rowcount == 0:
                return None
            return Produto(
                id_produto=produto_id,
                nome_produto=produto.nome_produto,
                descricao=produto.descricao,
                material=produto.material,
                altura=produto.altura,
                comprimento=produto.comprimento,
                largura=produto.largura,
                quantidade=produto.quantidade,
                peso=produto.peso,
                valor=produto.valor
            )

    async def delete_produto(self, produto_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM produtos WHERE id_produto = ?",
                (produto_id,)
            )
            return cursor.rowcount > 0