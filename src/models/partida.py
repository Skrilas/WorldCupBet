from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from datetime import datetime

class Partida(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    api_id: int = Field(unique=True, index=True)
    home_team_id: int = Field(foreign_key='time.id')
    away_team_id: int = Field(foreign_key='time.id')
    gols_home: int = Field(default=0)
    gols_away: int = Field(default=0)
    data_hora: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    terminou: bool = Field(default=False)
    vencedor_id: int | None = Field(foreign_key='time.id', default=None)
    aposta_ativa: bool = Field(default=False)