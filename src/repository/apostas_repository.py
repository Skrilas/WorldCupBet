from sqlmodel import Session
from models.apostas import Apostas

class ApostasRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def salvar(self, apostas: Apostas):
        self.session.add(apostas)

    def buscar_por_id(self, id: int):
        return self.session.get(Apostas, id)

    def excluir(self, id: id):
        apostas = self.buscar_por_id(id)
        if not apostas:
            raise ValueError("Aposta não encontrada.")
        self.session.delete(apostas)