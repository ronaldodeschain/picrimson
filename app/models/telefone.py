from pydantic import BaseModel

class Telefone(BaseModel):
    id_telefone:int
    telefone_principal:str
    telefone_secundario:str
    id_usuario:int

class TelefoneCriarAtualizar(BaseModel):
    telefone_principal:str
    telefone_secundario:str
    id_usuario:int