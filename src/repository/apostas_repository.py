from sqlmodel import Session, select
from models.apostas import Apostas

class ApostasRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def salvar(self, apostas: Apostas):
        self.session.add(apostas)

    def buscar_por_id_partida(self, id: int):
        statement = select(Apostas).where(Apostas.partida_id == id)
        return self.session.exec(statement).first()

    def excluir(self, id: id):
        apostas = self.buscar_por_id(id)
        if not apostas:
            raise ValueError("Aposta não encontrada.")
        self.session.delete(apostas)