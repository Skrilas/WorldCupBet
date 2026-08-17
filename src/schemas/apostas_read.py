from pydantic import BaseModel, ConfigDict
from decimal import Decimal

from src.enums.status_aposta import StatusAposta

class ApostasRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    partida_id: int
    time_id: int
    qtd_pontos: Decimal
    odd: Decimal
    status: StatusAposta
    pontos_ganhos: Decimal