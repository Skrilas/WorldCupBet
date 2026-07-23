from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class ApiPartida(BaseModel):
    api_id: int = Field(validation_alias="id")
    home_team_id: int
    away_team_id: int
    home_score: int
    away_score: int
    local_date: datetime
    finished: bool

    @field_validator("local_date", mode="before")
    @classmethod
    def converter_data(cls, value: str) -> datetime:
        return datetime.strptime(value, "%m/%d/%Y %H:%M")
