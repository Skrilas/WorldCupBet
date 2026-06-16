from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime
from datetime import datetime

class Partida(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    home_team_id: int = Field(foreign_key='time.id')
    away_team_id: int = Field(foreign_key='time.id')
    data_hora: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    terminou: bool = Field(default=False)
    vencedor: int | None = Field(default=None)