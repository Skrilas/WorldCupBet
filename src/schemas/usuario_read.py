from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class UsuarioRead(BaseModel):
    id: int
    nome: str
    email: str
    cpf: str
    data_nascimento: date
    pontos: Decimal
    palpites_corretos: int
    ativo: bool