from dataclasses import dataclass
from datetime import date

@dataclass
class usuario:
    nome: str
    email: str
    cpf: str
    data_nascimento: date
    login: str
    senha: str