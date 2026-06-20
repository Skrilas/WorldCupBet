from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint
from decimal import Decimal

from enum.status_aposta import StatusAposta

class Apostas(SQLModel, table=True):
    __table_args__ = (   # Impede registros duplicados para a combinação (usuario_id, partida_id).
    UniqueConstraint(
        "usuario_id",
        "partida_id"
        ),
    )
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id")
    partida_id: int = Field(foreign_key="partida.id")
    time_id: int = Field(foreign_key="time.id")
    qtd_pontos: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)
    odd: Decimal = Field(max_digits=10, decimal_places=2)
    status: StatusAposta = Field(default=StatusAposta.PENDENTE, max_length=20)
    pontos_ganhos: Decimal = Field(default=Decimal("0.00"), max_digits=12, decimal_places=2)