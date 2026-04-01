from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.imagem_produto import ImagemProduto, ImagemProdutoCriarAtualizar
from app.repositories.imagem_produto import ImagemProdutoRepository
from app.dependencies import get_imagem_produto_repository

router = APIRouter(prefix="/imagens_produto", tags=["Products"])

@router.get("/", response_model=List[ImagemProduto])
async def listar_imagens_produto(repo: ImagemProdutoRepository = Depends(get_imagem_produto_repository)):
    return await repo.listar_imagens_produto()

@router.get("/{imagem_id}", response_model=ImagemProduto)
async def get_imagem_produto(imagem_id: int, repo: ImagemProdutoRepository = Depends(get_imagem_produto_repository)):
    imagem = await repo.get_imagem_produto(imagem_id)
    if not imagem:
        raise HTTPException(status_code=404, detail="ImagemProduto not found")
    return imagem

@router.post("/", response_model=ImagemProduto)
async def criar_imagem_produto(imagem: ImagemProdutoCriarAtualizar, repo: ImagemProdutoRepository = Depends(get_imagem_produto_repository)):
    return await repo.criar_imagem_produto(imagem)

@router.put("/{imagem_id}", response_model=ImagemProduto)
async def update_imagem_produto(imagem_id: int, imagem: ImagemProdutoCriarAtualizar, repo: ImagemProdutoRepository = Depends(get_imagem_produto_repository)):
    updated_imagem = await repo.update_imagem_produto(imagem_id, imagem)
    if not updated_imagem:
        raise HTTPException(status_code=404, detail="ImagemProduto not found")
    return updated_imagem

@router.delete("/{imagem_id}")
async def delete_imagem_produto(imagem_id: int, repo: ImagemProdutoRepository = Depends(get_imagem_produto_repository)):
    deleted = await repo.delete_imagem_produto(imagem_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ImagemProduto not found")
    return {"message": "ImagemProduto deleted successfully"}