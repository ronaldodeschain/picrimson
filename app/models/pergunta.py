from pydantic import BaseModel

class Pergunta(BaseModel):
    id_pergunta: int
    pergunta: str
    data_criacao: str
    id_usuario: int
    id_produto: int
    id_resposta: int | None

class PerguntaCriarAtualizar(BaseModel):
    pergunta: str
    data_criacao: str
    id_usuario: int
    id_produto: int
    id_resposta: int | None = None
