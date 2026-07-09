from pydantic import BaseModel
from datetime import datetime

class ApostasAtivas(BaseModel):
    id: int
    home_team_id: int
    away_team_id: int
    home_team_name: str
    away_team_name: str
    local_date: datetime