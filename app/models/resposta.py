from pydantic import BaseModel

class Resposta(BaseModel):
    id_resposta: int
    texto_resposta: str
    data_resposta: str
    id_usuario: int
    id_produto: int
    id_pergunta: int | None = None

class RespostaCriarAtualizar(BaseModel):
    texto_resposta: str
    data_resposta: str
    id_usuario: int
    id_produto: int
    id_pergunta: int | None = None
