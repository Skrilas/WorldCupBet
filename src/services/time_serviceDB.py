from sqlmodel import Session
from database import engine

from models.time import Time
from repository.time_repository import TimeRepository

class TimeServiceDB:
    def criar_time(self, id_time, nome):
        with Session(engine) as session:
            repo = TimeRepository(session)

            novo_time = Time(
                id=id_time,
                nome=nome
            )
            return repo.salvar(novo_time)