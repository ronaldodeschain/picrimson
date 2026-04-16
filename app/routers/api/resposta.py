from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from app.models.resposta import RespostaCriarAtualizar
from app.repositories.resposta import RespostaRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/resposta",
    tags=["Answers"]
)

@router.get("/", response_model=list[RespostaCriarAtualizar])
async def listar_respostas(
    resposta_repository: Annotated[RespostaRepository, Depends(
        dependencies.get_resposta_repository
    )]
):
    return await resposta_repository.listar_respostas()

@router.get("/{resposta_id}", response_model=RespostaCriarAtualizar)
async def get_resposta(
    resposta_id: int,
    resposta_repository: Annotated[RespostaRepository, Depends(
        dependencies.get_resposta_repository
    )]
):
    resposta = await resposta_repository.get_resposta(resposta_id)
    if not resposta:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return resposta

@router.post("/", response_model=RespostaCriarAtualizar)
async def criar_resposta(
    resposta: RespostaCriarAtualizar,
    resposta_repository: Annotated[RespostaRepository, Depends(
        dependencies.get_resposta_repository
    )]
):
    return await resposta_repository.criar_resposta(resposta)

@router.put("/{resposta_id}", response_model=RespostaCriarAtualizar | None)
async def update_resposta(
    resposta_repository: Annotated[RespostaRepository, Depends(
        dependencies.get_resposta_repository
    )],
    resposta_id: int,
    resposta: RespostaCriarAtualizar
):
    resposta_atualizada = await resposta_repository.update_resposta(
        resposta_id, resposta
    )
    if not resposta_atualizada:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return resposta_atualizada

@router.delete("/{resposta_id}", status_code=204)
async def delete_resposta(
    resposta_repository: Annotated[RespostaRepository, Depends(
        dependencies.get_resposta_repository
    )],
    resposta_id: int
):
    success = await resposta_repository.delete_resposta(resposta_id)
    if not success:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return RedirectResponse(url="/resposta", status_code=303)
