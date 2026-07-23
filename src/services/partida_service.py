from sqlmodel import Session

from repository.partida_repository import PartidaRepository
from services.gerenciador_api_copa import GerenciadorApiCopa
from schemas.partida_read import PartidaRead
from schemas.api_partida import ApiPartida
from models.partida import Partida
from database import engine


class PartidaService:

    @staticmethod
    def criar_partidas() -> None:
        partidas = GerenciadorApiCopa.obter_api_partida_copa("games")
        with Session(engine) as session:
            repo = PartidaRepository(session)

            for p in partidas:
                api_partida = ApiPartida.model_validate(p)

                repo.salvar(
                    Partida(
                        api_id=api_partida.api_id,
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
    def mostrar_partida(id: int) -> PartidaRead:
        with Session(engine) as session:
            repo = PartidaRepository(session)
            resultado = repo.buscar_por_id_com_times(id)
            
            if resultado is None:
                raise ValueError("Partida não encontrada.")
            
            partida, home_name, away_name, vencedor_name = resultado
            
            return PartidaRead(
                id=partida.id,
                home_team_id=partida.home_team_id,
                away_team_id=partida.away_team_id,

                home_team_name=home_name,
                away_team_name=away_name,

                home_scorer=partida.gols_home,
                away_scorer=partida.gols_away,
                local_date=partida.data_hora,
                finished=partida.terminou,

                vencedor_id=partida.vencedor_id,
                vencedor_name=vencedor_name
            )


    @staticmethod
    def atualizar_resultado(partida: Partida, api_partida: ApiPartida, vencedor_id: int | None) -> None:
            
            partida.gols_away = api_partida.away_score
            partida.gols_home = api_partida.home_score
            partida.terminou = api_partida.finished
            partida.vencedor_id = vencedor_id