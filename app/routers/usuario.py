from typing import Annotated

from fastapi import APIRouter, Depends,HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.usuario import UsuarioCriarAtualizar
from app.repositories.usuario import UsuarioRepository
import app.dependencies as dependencies

router = APIRouter(
    prefix="/usuario"
)

templates = Jinja2Templates(directory="templates")

@router.get("/",response_model=list[UsuarioCriarAtualizar])
async def listar_usuarios(
    usuario_repository:Annotated[UsuarioRepository,Depends(
        dependencies.get_usuario_repository
    )]
):
    return await usuario_repository.listar_usuarios()

@router.post("/")
async def criar_usuario(
    usuario_repository:Annotated[UsuarioRepository,Depends(
        dependencies.get_usuario_repository
    )],
    request:Request,
    nome:str,
    email:str,
    senha:str,
    cpf:str):
    usuario_criar = UsuarioCriarAtualizar(
        nome_usuario=nome,
        login=email,
        senha=senha,
        cpf=cpf)
    usuario = await usuario_repository.criar_usuario(usuario_criar)