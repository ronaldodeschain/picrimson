import os
from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.models.produto import ProdutoCriarAtualizar
from app.models.imagem_produto import ImagemProdutoCriarAtualizar

class ProdutoService:
    def __init__(self, produto_repo, imagem_repo):
        self.produto_repo = produto_repo
        self.imagem_repo = imagem_repo

    async def cadastrar_produto(self, dados: ProdutoCriarAtualizar, arquivo: UploadFile = None, image_url: str | None = None):
        """Valida e persiste um produto com sua imagem."""
        if not dados.nome_produto or not dados.nome_produto.strip():
            return None, "O nome do produto é obrigatório."

        if dados.valor is None or dados.valor <= 0:
            return None, "O preço do produto deve ser maior que zero."

        if dados.quantidade is None or dados.quantidade < 0:
            return None, "A quantidade do produto não pode ser negativa."

        if image_url is not None and not isinstance(image_url, str):
            return None, "A URL da imagem deve ser uma string válida."

        if image_url is not None and image_url.strip() == "":
            return None, "A URL da imagem não pode estar vazia."
        # 1. Validação de Negócio: Preço
        if dados.valor < 0:
            return None, "O preço do produto não pode ser negativo."

        # 2. Salvar Produto
        produto = await self.produto_repo.criar_produto(dados)
        if not produto:
            return None, "Erro ao criar produto na base de dados."

        # 3. Lidar com Imagem
        if arquivo and arquivo.filename:
            uploads_dir = Path("app/static/uploads/produtos")
            uploads_dir.mkdir(parents=True, exist_ok=True)
            
            ext = Path(arquivo.filename).suffix
            nome_final = f"{uuid4().hex}{ext}"
            path_final = uploads_dir / nome_final
            
            with path_final.open("wb") as buffer:
                buffer.write(await arquivo.read())
            
            # Salvar referência no banco
            img_model = ImagemProdutoCriarAtualizar(
                nome_imagem=dados.nome_produto,
                arquivo_imagem=f"/static/uploads/produtos/{nome_final}",
                id_produto=produto.id_produto
            )
            await self.imagem_repo.criar_imagem_produto(img_model)

        elif image_url:
            img_model = ImagemProdutoCriarAtualizar(
                nome_imagem=dados.nome_produto,
                arquivo_imagem=image_url,
                id_produto=produto.id_produto
            )
            await self.imagem_repo.criar_imagem_produto(img_model)

        return produto, None