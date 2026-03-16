from pydantic import BaseModel

class Usuario(BaseModel):
    id_usuario:int 
    nome_usuario:str
    login:str
    senha:str
    cpf:str
