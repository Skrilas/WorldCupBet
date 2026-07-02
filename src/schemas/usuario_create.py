from pydantic import BaseModel
from datetime import date

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    cpf: str
    data_nascimento: date
    login: str
    senha: str