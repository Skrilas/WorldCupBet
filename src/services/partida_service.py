from sqlmodel import Session

from repository.partida_repository import PartidaRepository
from repository.time_repository import TimeRepository
from services.gerenciador_api import GerenciadorApi
from schemas.partida_read import PartidaRead
from schemas.api_partida import ApiPartida
from models.partida import Partida
from database import engine


class PartidaService:

    @staticmethod
    def criar_partidas():
        partidas = GerenciadorApi.obter_dados("games")
        with Session(engine) as session:
            repo = PartidaRepository(session)

            for p in partidas:
                api_partida = ApiPartida(**p)

                repo.salvar(
                    Partida(
                        home_team_id=api_partida.home_team_id,
                        away_team_id=api_partida.away_team_id,
                        gols_home=api_partida.home_scorers,
                        gols_away=api_partida.away_scorers,
                        data_hora=api_partida.local_date,
                        terminou=api_partida.finished
                    )
                )
            session.commit()

    @staticmethod
    def mostrar_partida(id: int):
        with Session(engine) as session:
            partida_repo = PartidaRepository(session)
            time_repo = TimeRepository(session)
            partida = partida_repo.buscar_por_id(id=id)
            
            if not partida:
                raise ValueError("Partida não encontrada.")
            
            home = time_repo.buscar_por_id(partida.home_team_id)
            away = time_repo.buscar_por_id(partida.away_team_id)
            vencedor = None #Caso o jogo empate ou não tenha terminado
            if partida.id_vencedor:
                vencedor = time_repo.buscar_por_id(partida.id_vencedor)
            
            return PartidaRead(
                id=partida.id,
                home_team_id=partida.home_team_id,
                away_team_id=partida.away_team_id,

                home_team_name=home.nome,
                away_team_name=away.nome,

                home_scorers=partida.gols_home,
                away_scorers=partida.gols_away,
                local_date=partida.data_hora,
                finished=partida.terminou,

                id_vencedor=partida.id_vencedor,
                vencedor_name=vencedor.nome if vencedor else None
            )


    @staticmethod
    def atualizar_status(id: int, terminou: bool, id_vencedor: int | None):
        with Session(engine) as session:
            repo = PartidaRepository(session)
            partida = repo.buscar_por_id(id=id)

            if not partida:
                raise ValueError("Partida não encontrada.")
            partida.terminou = terminou
            partida.id_vencedor = id_vencedor

            session.commit()