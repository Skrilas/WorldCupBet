from sqlmodel import Session
from src.database import engine

from src.services.gerenciador_api_historico import GerenciadoApiHistorico
from src.exceptions.business import BusinessRuleError, NotFoundError
from src.services.gerenciador_api_copa import GerenciadorApiCopa
from src.repository.time_repository import TimeRepository
from src.schemas.historico_copa import HistoricoCopa
from src.schemas.api_time import ApiTime
from src.models.time import Time

class TimeService:
    
    #USO ÚNICO PARA O PREENCHIMENTO DO BANCO!
    @staticmethod
    def criar_times() -> None:
        """Obtém os times da API externa e os cadastra no banco de dados."""
        times = GerenciadorApiCopa.obter_dados_copa("teams")
        with Session(engine) as session:
            repo = TimeRepository(session)

            for t in times:
                api_time = ApiTime(**t)  

                repo.salvar(
                    Time(
                        id=api_time.id,
                        nome=api_time.name
                        )
                )
            session.commit()

    @staticmethod
    def buscar_time_por_id(id: int) -> Time:
        """Retorna um time pelo seu identificador ou gera erro caso não seja encontrado."""
        with Session(engine) as session:
            repo = TimeRepository(session)

            time = repo.buscar_por_id(id)
            if not time:
                raise NotFoundError("Time não encontrado.")
            return time
        
    @staticmethod
    def listar_times() -> list[Time]:
        """Retorna todos os times cadastrados no banco de dados."""
        with Session(engine) as session:
            repo = TimeRepository(session)

            return repo.listar()
        
    @staticmethod
    def buscar_historico_copas(time_id: int) -> list[HistoricoCopa]:
        """Consulta e retorna o histórico de participações de um time em Copas do Mundo."""
        time = TimeService.buscar_time_por_id(time_id)

        historico_copas = GerenciadoApiHistorico.obter_historico_copas_time(time.nome)
        if not historico_copas["appearances"]:
            raise BusinessRuleError("O time não possui participações registradas em Copas do Mundo.")
        
        return TimeService._preencher_historico_copa(historico_copas["appearances"])
    
    @staticmethod
    def _preencher_historico_copa(appearances: list[dict]) -> list[HistoricoCopa]:
        """Converte os dados de participações da API em objetos HistoricoCopa."""
        historicos: list[HistoricoCopa] = []
        for appearance in appearances:
            group_stage = appearance["groupStage"]
            if group_stage is None:
                historicos.append(HistoricoCopa(
                ano=appearance["year"],
                colocacao=appearance["finalPosition"],
                jogos=None,
                vitorias=None,
                empates=None,
                derrotas=None,
                gols_pro=None,
                gols_contra=None,
                pontos=None
                    )
                )
            else:
                historicos.append(HistoricoCopa(
                ano=appearance["year"],
                colocacao=appearance["finalPosition"],
                jogos=group_stage["played"],
                vitorias=group_stage["won"],
                empates=group_stage["drawn"],
                derrotas=group_stage["lost"],
                gols_pro=group_stage.get("goalsFor", group_stage.get("gf")),
                gols_contra=group_stage.get("goalsAgainst", group_stage.get("ga")),
                pontos=group_stage.get("points", group_stage.get("pts"))
                    )
                )
        return historicos
