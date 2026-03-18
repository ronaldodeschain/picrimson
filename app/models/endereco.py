from pydantic import BaseModel

class Endereco(BaseModel):
    id_endereco: int
    rua: str
    numero: int
    complemento: str
    cep: str
    cidade: str
    estado: str
    observacoes: str
    id_usuario: int

class EnderecoCriarAtualizar(BaseModel):
    rua: str
    numero: int
    complemento: str
    cep: str
    cidade: str
    estado: str
    observacoes: str
    id_usuario: int
    
