from typing import Annotated

from fastapi import APIRouter, Depends,HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.usuario import UsuarioCriarAtualizar, UsuarioResposta
from app.repositories.usuario import UsuarioRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/usuario",
    tags=["User Management"]
)

templates = Jinja2Templates(directory="templates")

@router.get("/",response_model=list[UsuarioResposta])
async def listar_usuarios(
    usuario_repository:Annotated[UsuarioRepository,Depends(
        dependencies.get_usuario_repository
    )]
):
    return await usuario_repository.listar_usuarios()

@router.get("/{usuario_id}",response_model=UsuarioCriarAtualizar)
async def get_usuario(
    usuario_id:int,
    usuario_repository:Annotated[UsuarioRepository,Depends(
        dependencies.get_usuario_repository)]
):
    usuario = await usuario_repository.get_cliente(usuario_id)
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.post("/")
async def criar_usuario(
    usuario_repository:Annotated[UsuarioRepository,Depends(
        dependencies.get_usuario_repository
    )],
    request:Request,
    nome:str,
    email:str,
    senha:str,
    cpf:str,
    role:str = "user"):
    usuario_criar = UsuarioCriarAtualizar(
        nome_usuario=nome,
        login=email,
        senha=senha,
        cpf=cpf,
        role=role
    )
    usuario = await usuario_repository.criar_usuario(usuario_criar)
    return usuario

@router.put("/{usuario_id}",response_model=UsuarioCriarAtualizar | None)
async def update_usuario(
    usuario_repository:Annotated[UsuarioRepository,Depends(
        dependencies.get_usuario_repository)],
    usuario_id:int,
    usuario:UsuarioCriarAtualizar
):
    usuario_atualizado = await usuario_repository.update_usuario(
        usuario_id,usuario)
    if not usuario_atualizado:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario_atualizado

@router.delete("/{usuario_id}",status_code=204)
async def delete_usuario(
    usuario_repository:Annotated[UsuarioRepository,Depends(
        dependencies.get_usuario_repository)],
    usuario_id:int
):
    success = await usuario_repository.delete_usuario(usuario_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return RedirectResponse(url="/usuario", status_code=303)