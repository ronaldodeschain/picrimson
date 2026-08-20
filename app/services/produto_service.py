from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.models.produto import ProdutoCriarAtualizar
from app.models.imagem_produto import ImagemProdutoCriarAtualizar

UPLOADS_DIR = Path("app/static/uploads/produtos")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

class ProdutoService:
    def __init__(self, produto_repo, imagem_repo):
        self.produto_repo = produto_repo
        self.imagem_repo = imagem_repo

    async def cadastrar_produto(self, dados: ProdutoCriarAtualizar, arquivos: list[UploadFile] | None = None):
        if not dados.nome_produto or not dados.nome_produto.strip():
            return None, "O nome do produto é obrigatório."
        if not dados.valor or dados.valor <= 0:
            return None, "O preço do produto deve ser maior que zero."

        produto = await self.produto_repo.criar_produto(dados)
        if not produto:
            return None, "Erro ao criar produto na base de dados."

        if arquivos:
            UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
            for arquivo in arquivos:
                if not arquivo.filename:
                    continue
                ext = Path(arquivo.filename).suffix.lower()
                if ext not in ALLOWED_EXT:
                    continue
                nome_final = f"{uuid4().hex}{ext}"
                with (UPLOADS_DIR / nome_final).open("wb") as f:
                    f.write(await arquivo.read())
                await self.imagem_repo.criar_imagem_produto(ImagemProdutoCriarAtualizar(
                    nome_imagem=dados.nome_produto,
                    arquivo_imagem=f"/static/uploads/produtos/{nome_final}",
                    id_produto=produto.id_produto
                ))

        return produto, None
