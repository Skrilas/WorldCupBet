from sqlmodel import Session
from database import engine

from models.time import Time
from repository.time_repository import TimeRepository
from schemas.api_time import ApiTime
from services.gerenciador_api import GerenciadorApi

class TimeService:
    
    @staticmethod
    def criar_times():
        times = GerenciadorApi.obter_dados("teams")
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