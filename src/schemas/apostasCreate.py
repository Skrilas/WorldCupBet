from pydantic import BaseModel
from decimal import Decimal

class ApostasCreate(BaseModel):
    usuario_id: int
    partida_id: int
    time_id: int
    qtd_pontos: Decimal
    odd: Decimal