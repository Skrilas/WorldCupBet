from pydantic import BaseModel
from decimal import Decimal

class ApostasRead(BaseModel):
    id: int
    usuario_id: int
    partida_id: int
    time_id: int
    qtd_pontos: Decimal
    odd: Decimal