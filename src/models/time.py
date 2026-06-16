from sqlmodel import SQLModel, Field

class Time(SQLModel, table=True):
    id: int= Field(primary_key=True)
    nome: str = Field(max_length=100, unique=True)