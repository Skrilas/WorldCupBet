from sqlmodel import Session
from database import engine

from services.gerenciador_api_historico import GerenciadoApiHistorico
from services.gerenciador_api_copa import GerenciadorApiCopa
from repository.time_repository import TimeRepository
from schemas.historico_copa import HistoricoCopa
from schemas.api_time import ApiTime
from models.time import Time

class TimeService:
    
    #USO ÚNICO PARA O PREENCHIMENTO DO BANCO!
    @staticmethod
    def criar_times() -> None:
        times = GerenciadorApiCopa.obter_dados_copa("teams")
        with Session(engine) as session:
            repo = TimeRepository(session)

            for t in times:
                api_time = ApiTime(**t)  

                repo.salvar(
                    Time(
                        id=api_time.id,
                        nome=api_time.name_en
                        )
                )
            session.commit()

    @staticmethod
    def buscar_time_por_id(id: int) -> Time:
        with Session(engine) as session:
            repo = TimeRepository(session)

            time = repo.buscar_por_id(id)
            if not time:
                raise ValueError("Time não encontrado.")
            return time
        
    @staticmethod
    def listar_times() -> list[Time]:
        with Session(engine) as session:
            repo = TimeRepository(session)

            times = repo.listar()
            return [time
                     for time in times]
        
    @classmethod
    def buscar_historico_copas(cls, time_id: int) -> list[HistoricoCopa]:
        time = cls.buscar_time_por_id(time_id)

        historico_copas = GerenciadoApiHistorico.obter_historico_copas_time(time.nome)
        if not historico_copas["appearances"]:
            raise ValueError("O time não possui participações registradas em Copas do Mundo.")
        
        # return