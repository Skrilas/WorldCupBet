from pydantic import BaseModel, Field

class MultiplicadorAposta(BaseModel):
    id_partida: int
    multiplicador: int = Field(ge=2, le=5)