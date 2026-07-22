from pydantic import BaseModel

class Avaliacoes(BaseModel):
    id_avaliacao: int
    comentario: str
    avaliacao: float
    id_produto: int
    id_usuario: int
    destaque: bool = False

class AvaliacoesCriarAtualizar(BaseModel):
    comentario: str
    avaliacao: float
    id_produto: int
    id_usuario: int
    destaque: bool = False