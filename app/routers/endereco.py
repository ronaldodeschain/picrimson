from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.endereco import EnderecoCriarAtualizar
from app.repositories.endereco import EnderecoRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/endereco",
    tags=["User Management"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[EnderecoCriarAtualizar])
async def listar_enderecos(
    endereco_repository: Annotated[EnderecoRepository, Depends(
        dependencies.get_endereco_repository
    )]
):
    return await endereco_repository.listar_enderecos()

@router.get("/{endereco_id}", response_model=EnderecoCriarAtualizar)
async def get_endereco(
    endereco_id: int,
    endereco_repository: Annotated[EnderecoRepository, Depends(
        dependencies.get_endereco_repository
    )]
):
    endereco = await endereco_repository.get_endereco(endereco_id)

    if not endereco:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco

@router.post("/")
async def criar_endereco(
    endereco_repository: Annotated[EnderecoRepository, Depends(
        dependencies.get_endereco_repository
    )],
    request: Request,
    rua: str,
    numero: int,
    complemento: str,
    cep: str,
    cidade: str,
    estado: str,
    observacoes: str,
    id_usuario: int
):
    endereco_criar = EnderecoCriarAtualizar(
        rua=rua,
        numero=numero,
        complemento=complemento,
        cep=cep,
        cidade=cidade,
        estado=estado,
        observacoes=observacoes,
        id_usuario=id_usuario
    )
    endereco = await endereco_repository.criar_endereco(endereco_criar)
    return endereco

@router.put("/{endereco_id}", response_model=EnderecoCriarAtualizar | None)
async def update_endereco(
    endereco_repository: Annotated[EnderecoRepository, Depends(
        dependencies.get_endereco_repository
    )],
    endereco_id: int,
    endereco: EnderecoCriarAtualizar
):
    endereco_atualizado = await endereco_repository.update_endereco(
        endereco_id, endereco
    )
    if not endereco_atualizado:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco_atualizado

@router.delete("/{endereco_id}", status_code=204)
async def delete_endereco(
    endereco_repository: Annotated[EnderecoRepository, Depends(
        dependencies.get_endereco_repository
    )],
    endereco_id: int
):
    success = await endereco_repository.delete_endereco(endereco_id)
    if not success:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return RedirectResponse(url="/endereco", status_code=303)