from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    cpf: str
    data_nascimento: date
    login: str
    senha: str 
    pontos: Decimal = Decimal("100.00")
    palpites_corretos: int = 0
    ativo: bool = True