from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.telefone import TelefoneCriarAtualizar
from app.repositories.telefone import TelefoneRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/telefone",
    tags=["User Management"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[TelefoneCriarAtualizar])
async def listar_telefones(
    telefone_repository: Annotated[TelefoneRepository, Depends(
        dependencies.get_telefone_repository
    )]
):
    return await telefone_repository.listar_telefones()

@router.get("/{telefone_id}", response_model=TelefoneCriarAtualizar)
async def get_telefone(
    telefone_id: int,
    telefone_repository: Annotated[TelefoneRepository, Depends(
        dependencies.get_telefone_repository
    )]
):
    telefone = await telefone_repository.get_telefone(telefone_id)

    if not telefone:
        raise HTTPException(status_code=404, detail="Telefone não encontrado")
    return telefone

@router.post("/")
async def criar_telefone(
    telefone_repository: Annotated[TelefoneRepository, Depends(
        dependencies.get_telefone_repository
    )],
    request: Request,
    telefone_principal: int,
    telefone_secundario: int,
    id_usuario: int
):
    telefone_criar = TelefoneCriarAtualizar(
        telefone_principal=telefone_principal,
        telefone_secundario=telefone_secundario,
        id_usuario=id_usuario
    )
    telefone = await telefone_repository.criar_telefone(telefone_criar)
    return telefone

@router.put("/{telefone_id}", response_model=TelefoneCriarAtualizar | None)
async def update_telefone(
    telefone_repository: Annotated[TelefoneRepository, Depends(
        dependencies.get_telefone_repository
    )],
    telefone_id: int,
    telefone: TelefoneCriarAtualizar
):
    telefone_atualizado = await telefone_repository.update_telefone(
        telefone_id, telefone
    )
    if not telefone_atualizado:
        raise HTTPException(status_code=404, detail="Telefone não encontrado")
    return telefone_atualizado

@router.delete("/{telefone_id}", status_code=204)
async def delete_telefone(
    telefone_repository: Annotated[TelefoneRepository, Depends(
        dependencies.get_telefone_repository
    )],
    telefone_id: int
):
    success = await telefone_repository.delete_telefone(telefone_id)
    if not success:
        raise HTTPException(status_code=404, detail="Telefone não encontrado")
    return RedirectResponse(url="/telefone", status_code=303)