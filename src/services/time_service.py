import requests

from schemas.api_time import apiTime
from config.settings import settings

class TimeService:
    def obter_dados():
        response = requests.get(settings.api_jogos_url)

        if response.status_code != 200:
            raise Exception(f"Erro ao obter dados da API: {response.status_code}")
        
        dados = response.json()

        times_dict = {}

        for jogo in dados:
            
            times_dict[jogo["home_team_id"]] = jogo["home_team_name_en"]

            times_dict[jogo["away_team_id"]] = jogo["away_team_name_en"]
        
        return [
            apiTime(id=id_time, nome=nome)
            for id_time, nome in times_dict.items()
        ]