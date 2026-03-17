from pydantic import BaseModel


class Email(BaseModel):
    id_email:int
    email:str
    id_usuario:int

class EmailCriarAtualizar(BaseModel):
    email:str
    id_usuario:int
