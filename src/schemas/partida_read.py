from pydantic import BaseModel
from datetime import datetime

class PartidaRead(BaseModel):
    id: int
    home_team_id: int
    away_team_id: int

    home_team_name: str
    away_team_name: str

    home_scorers: int
    away_scorers: int
    local_date: datetime
    finished: bool

    id_vencedor: int | None
    vencedor_name: str | None