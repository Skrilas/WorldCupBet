from sqlmodel import SQLModel, Field
from datetime import date
from decimal import Decimal

class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100, unique=True)
    email: str = Field(max_length=255, unique=True)
    cpf: str = Field(max_length=11, unique=True)
    data_nascimento: date
    login: str = Field(max_length=30, unique=True)
    senha_hash: str = Field(max_length=255)
    pontos: Decimal = Field(default=Decimal("100.00"), max_digits=12, decimal_places=2)
    palpites_corretos: int = Field(default=0)
    ativo: bool = Field(default=True)
    admin: bool = Field(default=False)