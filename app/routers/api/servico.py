from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.servico import ServicoCriarAtualizar
from app.repositories.servico import ServicoRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/servico",
    tags=["Services"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[ServicoCriarAtualizar])
async def listar_servicos(
    servico_repository: Annotated[ServicoRepository, Depends(
        dependencies.get_servico_repository
    )]
):
    return await servico_repository.listar_servicos()

@router.get("/{servico_id}", response_model=ServicoCriarAtualizar)
async def get_servico(
    servico_id: int,
    servico_repository: Annotated[ServicoRepository, Depends(
        dependencies.get_servico_repository
    )]
):
    servico = await servico_repository.get_servico(servico_id)

    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return servico

@router.post("/")
async def criar_servico(
    servico_repository: Annotated[ServicoRepository, Depends(
        dependencies.get_servico_repository
    )],
    request: Request,
    tipo_servico: str,
    valor_servico: float,
    descricao: str,
    id_pedido: int,
    id_orcamento: int
):
    servico_criar = ServicoCriarAtualizar(
        tipo_servico=tipo_servico,
        valor_servico=valor_servico,
        descricao=descricao,
        id_pedido=id_pedido,
        id_orcamento=id_orcamento
    )
    servico = await servico_repository.criar_servico(servico_criar)
    return servico

@router.put("/{servico_id}", response_model=ServicoCriarAtualizar | None)
async def update_servico(
    servico_repository: Annotated[ServicoRepository, Depends(
        dependencies.get_servico_repository
    )],
    servico_id: int,
    servico: ServicoCriarAtualizar
):
    servico_atualizado = await servico_repository.update_servico(
        servico_id, servico
    )
    if not servico_atualizado:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return servico_atualizado

@router.delete("/{servico_id}", status_code=204)
async def delete_servico(
    servico_repository: Annotated[ServicoRepository, Depends(
        dependencies.get_servico_repository
    )],
    servico_id: int
):
    success = await servico_repository.delete_servico(servico_id)
    if not success:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return RedirectResponse(url="/servico", status_code=303)