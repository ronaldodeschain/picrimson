from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.nota_fiscal import NotaFiscal, NotaFiscalCriarAtualizar
from app.repositories.nota_fiscal import NotaFiscalRepository
from app.dependencies import get_nota_fiscal_repository

router = APIRouter(prefix="/notas_fiscais", tags=["Payments"])

@router.get("/", response_model=List[NotaFiscal])
async def listar_notas_fiscais(repo: NotaFiscalRepository = Depends(get_nota_fiscal_repository)):
    return await repo.listar_notas_fiscais()

@router.get("/{nota_id}", response_model=NotaFiscal)
async def get_nota_fiscal(nota_id: int, repo: NotaFiscalRepository = Depends(get_nota_fiscal_repository)):
    nota = await repo.get_nota_fiscal(nota_id)
    if not nota:
        raise HTTPException(status_code=404, detail="NotaFiscal not found")
    return nota

@router.post("/", response_model=NotaFiscal)
async def criar_nota_fiscal(nota: NotaFiscalCriarAtualizar, repo: NotaFiscalRepository = Depends(get_nota_fiscal_repository)):
    return await repo.criar_nota_fiscal(nota)

@router.put("/{nota_id}", response_model=NotaFiscal)
async def update_nota_fiscal(nota_id: int, nota: NotaFiscalCriarAtualizar, repo: NotaFiscalRepository = Depends(get_nota_fiscal_repository)):
    updated_nota = await repo.update_nota_fiscal(nota_id, nota)
    if not updated_nota:
        raise HTTPException(status_code=404, detail="NotaFiscal not found")
    return updated_nota

@router.delete("/{nota_id}")
async def delete_nota_fiscal(nota_id: int, repo: NotaFiscalRepository = Depends(get_nota_fiscal_repository)):
    deleted = await repo.delete_nota_fiscal(nota_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="NotaFiscal not found")
    return {"message": "NotaFiscal deleted successfully"}