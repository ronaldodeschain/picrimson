from typing import cast, Union
from app.database.local import Database as SQLiteDatabase
from app.database.crimson_database_pg import Database as PostgresDatabase
from app.models.produto import Produto, ProdutoCriarAtualizar
from app.models.imagem_produto import ImagemProduto

class ProdutoRepository:
    def __init__(self, db: Union[SQLiteDatabase, PostgresDatabase]):
        self.db = db

    async def listar_produtos(
        self,
        categoria: int | None = None,
        preco_min: float | None = None,
        preco_max: float | None = None,
        material: str | None = None
    ) -> list[Produto]:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            # JOIN para buscar a URL da primeira imagem associada ao produto
            # Use a subquery to get the first image per product (compatible with SQLite and Postgres)
            cursor.execute("""
                SELECT p.id_produto, p.nome_produto, p.descricao, p.material,
                       p.altura, p.comprimento, p.largura, p.quantidade, p.peso, p.valor,
                       p.id_categoria,
                       i.id_imagem_produto, i.nome_imagem, i.arquivo_imagem
                FROM produtos p
                LEFT JOIN imagem_produtos i ON i.id_imagem_produto = (
                    SELECT id_imagem_produto FROM imagem_produtos WHERE id_produto = p.id_produto ORDER BY id_imagem_produto LIMIT 1
                )
            """)
            linhas = cursor.fetchall()
            produtos = [
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
                    valor=linha[9],
                    id_categoria=linha[10],
                    imagens=[ImagemProduto(
                        id_imagem_produto=linha[11],
                        nome_imagem=linha[12],
                        arquivo_imagem=linha[13],
                        id_produto=linha[0]
                    )] if linha[11] else []
                ) for linha in linhas
            ]

            def aplica_filtro(p: Produto) -> bool:
                if categoria is not None and getattr(p, 'id_categoria', None) != categoria:
                    return False
                if material and material.lower() not in (p.material or '').lower():
                    return False
                if preco_min is not None and (p.valor is None or p.valor < preco_min):
                    return False
                if preco_max is not None and (p.valor is None or p.valor > preco_max):
                    return False
                return True

            return [p for p in produtos if aplica_filtro(p)]

    async def get_produto(self, produto_id: int) -> Produto | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            # Use subquery join and inline the id to avoid placeholder style differences between DB drivers
            cursor.execute(f"""
                SELECT p.id_produto, p.nome_produto, p.descricao, p.material,
                       p.altura, p.comprimento, p.largura, p.quantidade, p.peso, p.valor,
                       p.id_categoria,
                       i.id_imagem_produto, i.nome_imagem, i.arquivo_imagem
                FROM produtos p
                LEFT JOIN imagem_produtos i ON i.id_imagem_produto = (
                    SELECT id_imagem_produto FROM imagem_produtos WHERE id_produto = p.id_produto ORDER BY id_imagem_produto LIMIT 1
                )
                WHERE p.id_produto = {int(produto_id)}
            """)
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
                    valor=linha[9],
                    id_categoria=linha[10],
                    imagens=[ImagemProduto(
                        id_imagem_produto=linha[11],
                        nome_imagem=linha[12],
                        arquivo_imagem=linha[13],
                        id_produto=linha[0]
                    )] if linha[11] else []
                )
            return None

    async def criar_produto(self,
                            produto: ProdutoCriarAtualizar) -> Produto | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "INSERT INTO produtos(nome_produto, descricao, material, altura, comprimento, largura, quantidade, peso, valor, id_categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_produto",
                (produto.nome_produto, produto.descricao, produto.material, produto.altura, produto.comprimento, produto.largura, produto.quantidade, produto.peso, produto.valor, produto.id_categoria)
            )
            row = cursor.fetchone()
            if not row:
                return None
            id_produto = row[0]
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
                valor=produto.valor,
                id_categoria=produto.id_categoria,
                imagens=[]
            )

    async def update_produto(self, produto_id: int,
                             produto: ProdutoCriarAtualizar) -> Produto | None:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "UPDATE produtos SET nome_produto = %s, descricao = %s, material = %s, altura = %s, comprimento = %s, largura = %s, quantidade = %s, peso = %s, valor = %s, id_categoria = %s WHERE id_produto = %s",
                (produto.nome_produto, produto.descricao, produto.material, produto.altura, produto.comprimento, produto.largura, produto.quantidade, produto.peso, produto.valor, produto.id_categoria, produto_id)
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
                valor=produto.valor,
                id_categoria=produto.id_categoria,
                imagens=[]
            )

    async def delete_produto(self, produto_id: int) -> bool:
        with self.db.connect() as connexion:
            cursor = connexion.cursor()
            cursor.execute(
                "DELETE FROM produtos WHERE id_produto = %s",
                (produto_id,)
            )
            return cursor.rowcount > 0