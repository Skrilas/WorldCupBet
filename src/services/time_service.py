from sqlmodel import Session
from database import engine
import requests
import time
import urllib3

from models.time import Time
from repository.time_repository import TimeRepository
from schemas.api_time import ApiTime
from config.settings import settings
# usar a API-Football
#a api não tem certificado válidado, isso é pra não ficar dando msg de erro
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TimeService:
    @staticmethod
    def get_api(url: str, retries: int = 3, delay: int = 2):
        for attempt in range(retries):
            try:
                response = requests.get(
                    url,
                    timeout=10,
                    verify=False
                )

                if response.status_code == 200:
                    return response

                print(f"Tentativa {attempt + 1} falhou: {response.status_code}")

            except requests.RequestException as e:
                print(f"Erro na tentativa {attempt + 1}: {e}")

            time.sleep(delay)

        raise Exception("API indisponível após várias tentativas")

    @classmethod
    def obter_dados(cls):
        response = cls.get_api(settings.api_jogos_url)

        if response.status_code != 200:
            raise Exception(f"Erro ao obter dados da API: {response.status_code}")
        
        try:
            dados = response.json()
        except Exception:
            raise Exception("Resposta da API não é JSON válido")

        times_dict = {}

        if "games" not in dados:
            raise Exception("Resposta da API não contém a chave 'games'")

        for jogo in dados["games"]:
            
            times_dict[jogo["home_team_id"]] = jogo["home_team_name_en"]

            times_dict[jogo["away_team_id"]] = jogo["away_team_name_en"]
        
        return [
            ApiTime(id=id_time, nome=nome)
            for id_time, nome in times_dict.items()
        ]
    
    @classmethod
    def criar_times(cls):
        times = cls.obter_dados()
        with Session(engine) as session:
            repo = TimeRepository(session)

            for time in times:  
                novo_time = Time(**time.model_dump())
                repo.salvar(novo_time)
            session.commit()