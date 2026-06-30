from dataclasses import dataclass

@dataclass
class OverviewApostas:
    total_apostadores: int
    total_pontos: int
    away_team_name: str
    home_team_name: str
    total_pontos_away: int
    total_pontos_home: int