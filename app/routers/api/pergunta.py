from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from app.models.pergunta import PerguntaCriarAtualizar
from app.repositories.pergunta import PerguntaRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/pergunta",
    tags=["Questions"]
)

@router.get("/", response_model=list[PerguntaCriarAtualizar])
async def listar_perguntas(
    pergunta_repository: Annotated[PerguntaRepository, Depends(
        dependencies.get_pergunta_repository
    )]
):
    return await pergunta_repository.listar_perguntas()

@router.get("/{pergunta_id}", response_model=PerguntaCriarAtualizar)
async def get_pergunta(
    pergunta_id: int,
    pergunta_repository: Annotated[PerguntaRepository, Depends(
        dependencies.get_pergunta_repository
    )]
):
    pergunta = await pergunta_repository.get_pergunta(pergunta_id)
    if not pergunta:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return pergunta

@router.post("/")
async def criar_pergunta(
    pergunta_repository: Annotated[PerguntaRepository, Depends(
        dependencies.get_pergunta_repository
    )],
    request: Request,
    pergunta: str,
    data_criacao: str,
    id_usuario: int,
    id_produto: int,
    id_resposta: int | None = None
):
    pergunta_criar = PerguntaCriarAtualizar(
        pergunta=pergunta,
        data_criacao=data_criacao,
        id_usuario=id_usuario,
        id_produto=id_produto,
        id_resposta=id_resposta
    )
    return await pergunta_repository.criar_pergunta(pergunta_criar)

@router.put("/{pergunta_id}", response_model=PerguntaCriarAtualizar | None)
async def update_pergunta(
    pergunta_repository: Annotated[PerguntaRepository, Depends(
        dependencies.get_pergunta_repository
    )],
    pergunta_id: int,
    pergunta: PerguntaCriarAtualizar
):
    pergunta_atualizada = await pergunta_repository.update_pergunta(
        pergunta_id, pergunta
    )
    if not pergunta_atualizada:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return pergunta_atualizada

@router.delete("/{pergunta_id}", status_code=204)
async def delete_pergunta(
    pergunta_repository: Annotated[PerguntaRepository, Depends(
        dependencies.get_pergunta_repository
    )],
    pergunta_id: int
):
    success = await pergunta_repository.delete_pergunta(pergunta_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pergunta não encontrada")
    return RedirectResponse(url="/pergunta", status_code=303)
