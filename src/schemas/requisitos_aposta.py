from pydantic import BaseModel
from decimal import Decimal

class RequisitosAposta(BaseModel):
    id_partida: int
    id_time: int
    pontos_apostados: Decimal