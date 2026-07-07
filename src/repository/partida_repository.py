from sqlmodel import Session, select
from sqlalchemy.orm import aliased

from models.partida import Partida
from models.time import Time

class PartidaRepository:
    def __init__(self, session: Session):
        self.session = session

    def salvar(self, partida: Partida):
        self.session.add(partida)

    def buscar_por_id(self, id: int) -> Partida | None:
        return self.session.get(Partida, id)
    
    def listar(self) -> list[Partida]:
        return self.session.exec(select(Partida)).all()

    def excluir(self, id: int):
        partida = self.buscar_por_id(id=id)
        if not partida:
            raise ValueError("Partida não encontrada.")
        self.session.delete(partida)
    
    def __consulta_com_times(self):
        home = aliased(Time)
        away = aliased(Time)
        winner = aliased(Time)

        statement = select(Partida,
                            home.nome.label("home_name"),
                            away.nome.label("away_name"),
                            winner.nome.label("winner_name")
                            ).join(home, Partida.home_team_id == home.id
                                ).join(away, Partida.away_team_id == away.id
                                       ).outerjoin(winner, Partida.vencedor_id == winner.id)
        return statement
    
    def mostrar_partidas_ativas(self) -> list[tuple[Partida, str, str, str | None]]:
        statement = self.__consulta_com_times()
        
        return self.session.exec(statement.where(Partida.aposta_ativa)).all()

    def buscar_por_id_com_times(self, id: int) -> tuple[Partida, str, str, str | None]| None:
        statement = self.__consulta_com_times()
        
        return self.session.exec(statement.where(Partida.id == id)).first()