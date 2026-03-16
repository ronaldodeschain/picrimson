from pydantic import BaseModel

class Carrinho(BaseModel):
    id_carrinho:int
    id_servico:int
    id_pedido:int
    id_item_pedido:int
    id_usuario:int