from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.cupom import CupomCriarAtualizar
from app.repositories.cupom import CupomRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/cupom",
    tags=["Orders"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[CupomCriarAtualizar])
async def listar_cupons(
    cupom_repository: Annotated[CupomRepository, Depends(
        dependencies.get_cupom_repository
    )]
):
    return await cupom_repository.listar_cupons()

@router.get("/{cupom_id}", response_model=CupomCriarAtualizar)
async def get_cupom(
    cupom_id: int,
    cupom_repository: Annotated[CupomRepository, Depends(
        dependencies.get_cupom_repository
    )]
):
    cupom = await cupom_repository.get_cupom(cupom_id)

    if not cupom:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return cupom

@router.post("/")
async def criar_cupom(
    cupom_repository: Annotated[CupomRepository, Depends(
        dependencies.get_cupom_repository
    )],
    request: Request,
    chave_cupom: str,
    valor_cupom: float,
    tipo_cupom: str,
    id_pedido: int
):
    cupom_criar = CupomCriarAtualizar(
        chave_cupom=chave_cupom,
        valor_cupom=valor_cupom,
        tipo_cupom=tipo_cupom,
        id_pedido=id_pedido
    )
    cupom = await cupom_repository.criar_cupom(cupom_criar)
    return cupom

@router.put("/{cupom_id}", response_model=CupomCriarAtualizar | None)
async def update_cupom(
    cupom_repository: Annotated[CupomRepository, Depends(
        dependencies.get_cupom_repository
    )],
    cupom_id: int,
    cupom: CupomCriarAtualizar
):
    cupom_atualizado = await cupom_repository.update_cupom(
        cupom_id, cupom
    )
    if not cupom_atualizado:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return cupom_atualizado

@router.delete("/{cupom_id}", status_code=204)
async def delete_cupom(
    cupom_repository: Annotated[CupomRepository, Depends(
        dependencies.get_cupom_repository
    )],
    cupom_id: int
):
    success = await cupom_repository.delete_cupom(cupom_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return RedirectResponse(url="/cupom", status_code=303)