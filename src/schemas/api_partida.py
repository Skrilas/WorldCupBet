from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class ApiPartida(BaseModel):
    api_id: int
    home_team_id: int
    away_team_id: int
    home_score: int
    away_score: int
    utc_date: datetime
    finished: bool

    @classmethod
    def converter_api(cls, p: dict) -> "ApiPartida":
        return cls(
            api_id=p["id"],
            home_team_id=p["homeTeam"]["id"],
            away_team_id=p["awayTeam"]["id"],
            home_score=p["score"]["fullTime"]["home"],
            away_score=p["score"]["fullTime"]["away"],
            utc_date=p["utcDate"],
            finished=p["status"] == "FINISHED"
        )