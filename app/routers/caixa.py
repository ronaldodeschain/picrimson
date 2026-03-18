from typing import Annotated, Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.caixa import CaixaCriarAtualizar
from app.repositories.caixa import CaixaRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/caixa",
    tags=["Payments"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[CaixaCriarAtualizar])
async def listar_caixas(
    caixa_repository: Annotated[CaixaRepository, Depends(
        dependencies.get_caixa_repository
    )]
):
    return await caixa_repository.listar_caixas()

@router.get("/{caixa_id}", response_model=CaixaCriarAtualizar)
async def get_caixa(
    caixa_id: int,
    caixa_repository: Annotated[CaixaRepository, Depends(
        dependencies.get_caixa_repository
    )]
):
    caixa = await caixa_repository.get_caixa(caixa_id)

    if not caixa:
        raise HTTPException(status_code=404, detail="Caixa não encontrada")
    return caixa

@router.post("/")
async def criar_caixa(
    caixa_repository: Annotated[CaixaRepository, Depends(
        dependencies.get_caixa_repository
    )],
    request: Request,
    tipo_movimentacao: str,
    valor: float,
    descricao: str,
    data_movimentacao: Optional[date] = None,
    id_nota_fiscal: int = 0,
    id_pagamento: int = 0
):
    caixa_criar = CaixaCriarAtualizar(
        tipo_movimentacao=tipo_movimentacao,
        valor=valor,
        descricao=descricao,
        data_movimentacao=data_movimentacao,
        id_nota_fiscal=id_nota_fiscal,
        id_pagamento=id_pagamento
    )
    caixa = await caixa_repository.criar_caixa(caixa_criar)
    return caixa

@router.put("/{caixa_id}", response_model=CaixaCriarAtualizar | None)
async def update_caixa(
    caixa_repository: Annotated[CaixaRepository, Depends(
        dependencies.get_caixa_repository
    )],
    caixa_id: int,
    caixa: CaixaCriarAtualizar
):
    caixa_atualizado = await caixa_repository.update_caixa(
        caixa_id, caixa
    )
    if not caixa_atualizado:
        raise HTTPException(status_code=404, detail="Caixa não encontrada")
    return caixa_atualizado

@router.delete("/{caixa_id}", status_code=204)
async def delete_caixa(
    caixa_repository: Annotated[CaixaRepository, Depends(
        dependencies.get_caixa_repository
    )],
    caixa_id: int
):
    success = await caixa_repository.delete_caixa(caixa_id)
    if not success:
        raise HTTPException(status_code=404, detail="Caixa não encontrada")
    return RedirectResponse(url="/caixa", status_code=303)