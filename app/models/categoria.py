from pydantic import BaseModel

class Categoria(BaseModel):
    id_categoria:int
    nome_categoria:str