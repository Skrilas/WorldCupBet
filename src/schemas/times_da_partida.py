from dataclasses import dataclass

from models.time import Time

@dataclass(frozen=True)
class TimesDaPartida:
    home_team: Time
    away_team: Time