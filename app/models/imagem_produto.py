from pydantic import BaseModel

class ImagemProduto(BaseModel):
    id_imagem_produto:int
    nome_imagem:str
    arquivo_imagem:str
    id_produto:int