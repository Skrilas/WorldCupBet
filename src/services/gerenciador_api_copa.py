from urllib.parse import quote
import requests

from src.exceptions.business import ExternalApiError
from src.config.settings import settings

class GerenciadorApiCopa:
    headers = { "X-Auth-Token": settings.api_token}
    @classmethod
    def obter_dados_copa(cls, tipo: str):
        """Consulta a API externa de futebol e retorna os dados solicitados."""
        
        endpoint = f"{settings.api_url}{quote(tipo)}" #configura url pra receber o json de um dado da API
        try:
            response = requests.get(endpoint, headers=cls.headers, timeout=20)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ExternalApiError(f"Erro ao acessar a API: {e}") from e
        
        dados = response.json()
        if tipo not in dados:
            raise ExternalApiError(f"A resposta da API não contém a chave '{tipo}'")
        return dados[tipo]