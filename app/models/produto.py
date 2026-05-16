from pydantic import BaseModel
from app.models.imagem_produto import ImagemProduto

class Produto(BaseModel):
    id_produto:int
    nome_produto:str
    descricao:str
    material:str
    altura:float
    comprimento:float
    largura:float
    quantidade:int
    peso:float
    valor:float
    id_categoria: int | None = None
    imagens: list[ImagemProduto] = []

class ProdutoCriarAtualizar(BaseModel):
    nome_produto:str
    descricao:str
    material:str
    altura:float
    comprimento:float
    largura:float
    quantidade:int
    peso:float
    valor:float
    id_categoria: int | None = None