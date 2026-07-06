from sqlmodel import Session
from models.time import Time

class TimeRepository:
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, time: Time):
        self.session.add(time)

        return time
    
    def buscar_por_id(self, id: int) -> Time | None:
        return self.session.get(Time, id)