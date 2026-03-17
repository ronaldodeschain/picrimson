from pydantic import BaseModel

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