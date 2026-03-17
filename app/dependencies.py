from typing import Annotated
from fastapi import Depends

from app.database.local import Database
from app.repositories.usuario import UsuarioRepository


db = Database()

def get_database() -> Database:
    return db

def get_usuario_repository(
    Local_db: Annotated[Database,Depends(get_database)]
) -> UsuarioRepository:
    return UsuarioRepository(Local_db)