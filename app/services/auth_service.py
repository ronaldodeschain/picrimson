from typing import Annotated
from fastapi import Request, Depends
from app.repositories.usuario import UsuarioRepository
import app.dependencies as dependencies


async def get_authenticated_usuario(request: Request, usuario_repo: Annotated[UsuarioRepository, Depends(dependencies.get_usuario_repository)]):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return await usuario_repo.get_cliente(user_id)
