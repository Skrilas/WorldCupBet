from sqlmodel import Session, select
from sqlalchemy import func

from src.schemas.estatistica_aposta import EstatisticaAposta
from src.enums.status_aposta import StatusAposta
from src.models.apostas import Apostas

class ApostasRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def salvar(self, apostas: Apostas):
        self.session.add(apostas)

    def buscar_por_id_partida(self, id_partida: int, id_usuario: int) -> Apostas | None:
        statement = select(Apostas).where(Apostas.partida_id == id_partida, Apostas.usuario_id == id_usuario )
        return self.session.exec(statement).first()

    def listar_por_id_partida(self, id_partida: int) -> list[Apostas]:
            statement = select(Apostas).where(Apostas.partida_id == id_partida)
            return self.session.exec(statement).all()
    
    def listar(self, id_usuario) -> list[Apostas]:
        return self.session.exec(select(Apostas).where(Apostas.usuario_id == id_usuario)).all()

    def excluir(self, id: id):
        apostas = self.buscar_por_id(id)
        if not apostas:
            raise ValueError("Aposta não encontrada.")
        self.session.delete(apostas)

    def possui_apostas_pendentes(self, id_usuario) -> bool:
        statement = select(Apostas).where(Apostas.usuario_id == id_usuario, Apostas.status == StatusAposta.PENDENTE)
        return self.session.exec(statement).first() is not None
     
    def obter_estatisticas_aposta(self, id_partida: int) -> list[EstatisticaAposta]: #não retorna a odd, pois a odd é um dado único por usuário
        statement = (
            select(
                Apostas.time_id,
                func.count().label("total_apostadores"),
                func.sum(Apostas.qtd_pontos).label("total_pontos")
            )
            .where(Apostas.partida_id == id_partida)
            .group_by(Apostas.time_id)
        )
        resultado = self.session.exec(statement).all()

        return [EstatisticaAposta(**linha._mapping) for linha in resultado]