from sqlmodel import Session
from database import engine
import requests

from models.time import Time
from repository.time_repository import TimeRepository
from schemas.api_time import ApiTime
from config.settings import settings

class TimeService:
    @classmethod
    def obter_dados(cls):
        headers = {
            "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
            )}
        endpoint = f"{settings.api_url}teams" #configura url pra receber o json dos times
        try:
            response = requests.get(endpoint, headers=headers, timeout=20)
            response.raise_for_status()
            
        except requests.RequestException as e:
            raise Exception(f"Erro ao acessar a API: {e}")
        
        dados = response.json()
        if "teams" not in dados:
            raise Exception("A resposta da API não contém a chave 'teams'.")

        return dados["teams"]
            
    
    @classmethod
    def criar_times(cls):
        times = cls.obter_dados()
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