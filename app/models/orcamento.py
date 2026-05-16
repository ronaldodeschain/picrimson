from pydantic import BaseModel

class Orcamento(BaseModel):
    id_orcamento: int
    mensagem: str | None = None
    arquivo: str | None = None
    imagem: str | None = None
    id_mensagem: int | None = None
    id_servico: int | None = None
    nome: str | None = None
    contato: str | None = None
    tipo_projeto: str | None = None
    descricao: str | None = None
    tamanho_desejado: str | None = None

class OrcamentoCriarAtualizar(BaseModel):
    mensagem: str | None = None
    arquivo: str | None = None
    imagem: str | None = None
    id_mensagem: int | None = None
    id_servico: int | None = None
    nome: str | None = None
    contato: str | None = None
    tipo_projeto: str | None = None
    descricao: str | None = None
    tamanho_desejado: str | None = None