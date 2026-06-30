from sqlmodel import Session, select
from sqlalchemy import func
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
     
    def estatisticas_aposta_partida(self, id_partida: int): #não retorna a odd, pois a odd é um dado único por usuário
        statement = (
            select(
                Apostas.time_id,
                func.count().label("total_apostadores"),
                func.sum(Apostas.qtd_pontos).label("total_pontos")
            )
            .where(Apostas.partida_id == id_partida)
            .group_by(Apostas.time_id)
        )
        return self.session.exec(statement).all()