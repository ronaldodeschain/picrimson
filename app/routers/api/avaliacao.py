from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.avaliacoes import AvaliacoesCriarAtualizar
from app.repositories.avaliacoes import AvaliacoesRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/avaliacao",
    tags=["Reviews"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=list[AvaliacoesCriarAtualizar])
async def listar_avaliacoes(
    avaliacao_repository: Annotated[AvaliacoesRepository, Depends(
        dependencies.get_avaliacoes_repository
    )]
):
    return await avaliacao_repository.listar_avaliacoes()

@router.get("/{avaliacao_id}", response_model=AvaliacoesCriarAtualizar)
async def get_avaliacao(
    avaliacao_id: int,
    avaliacao_repository: Annotated[AvaliacoesRepository, Depends(
        dependencies.get_avaliacoes_repository
    )]
):
    avaliacao = await avaliacao_repository.get_avaliacao(avaliacao_id)

    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao

@router.post("/")
async def criar_avaliacao(
    avaliacao_repository: Annotated[AvaliacoesRepository, Depends(
        dependencies.get_avaliacoes_repository
    )],
    request: Request,
    comentario: str,
    avaliacao: float,
    id_produto: int,
    id_usuario: int
):
    avaliacao_criar = AvaliacoesCriarAtualizar(
        comentario=comentario,
        avaliacao=avaliacao,
        id_produto=id_produto,
        id_usuario=id_usuario
    )
    nova_avaliacao = await avaliacao_repository.criar_avaliacao(avaliacao_criar)
    return nova_avaliacao

@router.put("/{avaliacao_id}", response_model=AvaliacoesCriarAtualizar | None)
async def update_avaliacao(
    avaliacao_repository: Annotated[AvaliacoesRepository, Depends(
        dependencies.get_avaliacoes_repository
    )],
    avaliacao_id: int,
    avaliacao: AvaliacoesCriarAtualizar
):
    avaliacao_atualizado = await avaliacao_repository.update_avaliacao(
        avaliacao_id, avaliacao
    )
    if not avaliacao_atualizado:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao_atualizado

@router.delete("/{avaliacao_id}", status_code=204)
async def delete_avaliacao(
    avaliacao_repository: Annotated[AvaliacoesRepository, Depends(
        dependencies.get_avaliacoes_repository
    )],
    avaliacao_id: int
):
    success = await avaliacao_repository.delete_avaliacao(avaliacao_id)
    if not success:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return RedirectResponse(url="/avaliacao", status_code=303)