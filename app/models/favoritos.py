from pydantic import BaseModel

class Favoritos(BaseModel):
    id_favoritos:int
    id_produto:int
    id_usuario:int

class FavoritosCriarAtualizar(BaseModel):
    id_produto:int
    id_usuario:int