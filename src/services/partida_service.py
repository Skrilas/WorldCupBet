from sqlmodel import Session

from src.repository.partida_repository import PartidaRepository
from src.services.gerenciador_api_copa import GerenciadorApiCopa
from src.exceptions.business import NotFoundError
from src.schemas.partida_read import PartidaRead
from src.schemas.api_partida import ApiPartida
from src.models.partida import Partida
from src.database import engine


class PartidaService:

    @staticmethod
    #USO ÚNICO PARA O PREENCHIMENTO DO BANCO!
    def criar_partidas() -> None:
        """Obtém as partidas da API externa e as cadastra no banco de dados."""
        partidas = GerenciadorApiCopa.obter_dados_copa("matches")
        with Session(engine) as session:
            repo = PartidaRepository(session)

            for p in partidas:
                api_partida = ApiPartida.converter_api(p)

                repo.salvar(
                    Partida(
                        api_id=api_partida.api_id,
                        home_team_id=api_partida.home_team_id,
                        away_team_id=api_partida.away_team_id,
                        gols_home=api_partida.home_score,
                        gols_away=api_partida.away_score,
                        data_hora=api_partida.utc_date,
                        terminou=api_partida.finished
                    )
                )
            session.commit()

    @staticmethod
    def listar_partidas() -> list[Partida]:
        """Retorna todas as partidas cadastradas no banco de dados."""
        with Session(engine) as session:
            repo = PartidaRepository(session)

            return repo.listar()

    @staticmethod
    def mostrar_partida(id: int) -> PartidaRead:
        """Retorna os dados de uma partida, incluindo os nomes dos times e do vencedor."""
        with Session(engine) as session:
            repo = PartidaRepository(session)
            resultado = repo.buscar_por_api_id_com_times(id)
            
            if resultado is None:
                raise NotFoundError("Partida não encontrada.")
            
            partida, home_name, away_name, vencedor_name = resultado
            
            return PartidaRead(
                id=partida.id,
                home_team_id=partida.home_team_id,
                away_team_id=partida.away_team_id,

                home_team_name=home_name,
                away_team_name=away_name,

                home_score=partida.gols_home,
                away_score=partida.gols_away,
                utc_date=partida.data_hora,
                finished=partida.terminou,

                vencedor_id=partida.vencedor_id,
                vencedor_name=vencedor_name
            )


    @staticmethod
    def atualizar_resultado(partida: Partida, api_partida: ApiPartida, vencedor_id: int | None) -> None:
            """Atualiza o resultado de uma partida com os dados obtidos da API externa."""
            
            partida.gols_away = api_partida.away_score
            partida.gols_home = api_partida.home_score
            partida.terminou = api_partida.finished
            partida.vencedor_id = vencedor_id