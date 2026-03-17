from pydantic import BaseModel

class Usuario(BaseModel):
    id_usuario:int | None = None
    nome_usuario:str
    login:str
    senha:str
    cpf:str

class UsuarioCriarAtualizar(BaseModel):
    nome_usuario:str
    login:str
    senha:str
    cpf:str