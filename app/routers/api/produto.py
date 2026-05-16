from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.produto import ProdutoCriarAtualizar
from app.repositories.produto import ProdutoRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/produto",
    tags=["Products"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[ProdutoCriarAtualizar])
async def listar_produtos(
    produto_repository: Annotated[ProdutoRepository, Depends(
        dependencies.get_produto_repository
    )]
):
    return await produto_repository.listar_produtos()

@router.get("/{produto_id}", response_model=ProdutoCriarAtualizar)
async def get_produto(
    produto_id: int,
    produto_repository: Annotated[ProdutoRepository, Depends(
        dependencies.get_produto_repository
    )]
):
    produto = await produto_repository.get_produto(produto_id)

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/")
async def criar_produto(
    produto_repository: Annotated[ProdutoRepository, Depends(
        dependencies.get_produto_repository
    )],
    request: Request,
    nome_produto: str,
    descricao: str,
    material: str,
    altura: float,
    comprimento: float,
    largura: float,
    quantidade: int,
    peso: float,
    valor: float,
    id_categoria: int | None = None
):
    produto_criar = ProdutoCriarAtualizar(
        nome_produto=nome_produto,
        descricao=descricao,
        material=material,
        altura=altura,
        comprimento=comprimento,
        largura=largura,
        quantidade=quantidade,
        peso=peso,
        valor=valor,
        id_categoria=id_categoria
    )
    produto = await produto_repository.criar_produto(produto_criar)
    return produto

@router.put("/{produto_id}", response_model=ProdutoCriarAtualizar | None)
async def update_produto(
    produto_repository: Annotated[ProdutoRepository, Depends(
        dependencies.get_produto_repository
    )],
    produto_id: int,
    produto: ProdutoCriarAtualizar
):
    produto_atualizado = await produto_repository.update_produto(
        produto_id, produto
    )
    if not produto_atualizado:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto_atualizado

@router.delete("/{produto_id}", status_code=204)
async def delete_produto(
    produto_repository: Annotated[ProdutoRepository, Depends(
        dependencies.get_produto_repository
    )],
    produto_id: int
):
    success = await produto_repository.delete_produto(produto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return RedirectResponse(url="/produto", status_code=303)