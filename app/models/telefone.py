from pydantic import BaseModel

class Telefone(BaseModel):
    id_telefone:int
    telefone_principal:int
    telefone_secundario:int
    id_usuario:int

class TelefoneCriarAtualizar(BaseModel):
    telefone_principal:int
    telefone_secundario:int
    id_usuario:int