from sqlmodel import Session, select

from models.time import Time

class TimeRepository:
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, time: Time):
        self.session.add(time)

        return time
    
    def buscar_por_id(self, id: int) -> Time | None:
        return self.session.get(Time, id)
    
    def listar(self) -> list[Time]:
        return self.session.exec(select(Time)).all()