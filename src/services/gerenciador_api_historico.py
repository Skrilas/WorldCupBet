from urllib.parse import quote
import requests

from config.settings import settings

class GerenciadoApiHistorico:
    
    @staticmethod
    def obter_historico_copas_time(time: str):
        headers = {
            "X-API-Key": settings.historico_api_key
        }
        endpoint = f"{settings.historico_api_url}{quote(time)}" #configura url pra receber o json das partidas

        try:
            response = requests.get(endpoint, headers=headers, timeout=20)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Erro ao acessar a API: {e}") from e
        
        historico = response.json()
        return historico