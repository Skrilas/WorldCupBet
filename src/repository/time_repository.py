from sqlmodel import Session
from models.time import Time

class TimeRepository:
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, time: Time):
        self.session.add(time)
        self.session.commit()
        self.session.refresh(time)

        return time