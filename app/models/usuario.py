from pydantic import BaseModel

class Usuario(BaseModel):
    id_usuario:int | None = None
    nome_usuario:str
    login:str
    senha:str
    cpf:str | None = None
    autenticado:str = "nao_autenticado"
    role:str = "user"

class UsuarioCriarAtualizar(BaseModel):
    nome_usuario:str
    login:str
    senha:str
    cpf:str | None = None
    autenticado:str = "nao_autenticado"
    role:str = "user"

class UsuarioResposta(BaseModel):
    id_usuario:int
    nome_usuario:str
    login:str
    cpf:str | None = None
    role:str