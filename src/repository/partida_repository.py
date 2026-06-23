from sqlmodel import Session
from models.partida import Partida

class PartidaRepository:
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, partida: Partida):
        self.session.add(partida)

    def buscar_por_id(self, id: int):
        return self.session.get(Partida, id)

    def excluir(self, id: int):
        partida = self.buscar_por_id(id=id)
        if not partida:
            raise ValueError("Partida não encontrada.")
        self.session.delete(partida)