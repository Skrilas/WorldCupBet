from pydantic import BaseModel
from decimal import Decimal

class EstatisticaAposta(BaseModel):
    time_id: int
    total_apostadores: int
    total_pontos: Decimal