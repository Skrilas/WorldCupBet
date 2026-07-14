from pydantic import BaseModel 
from decimal import Decimal

class RankingUsuario(BaseModel):
    nome: str
    pontos: Decimal
    palpites_corretos: int