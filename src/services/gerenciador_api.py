from config.settings import settings
import requests

class GerenciadorApi:
    headers = { #simular um navegador pra obter dados da api
            "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
            )}
    @classmethod
    def obter_dados(cls, tipo: str):
        
        endpoint = f"{settings.api_url}{tipo}" #configura url pra receber o json das partidas
        try:
            response = requests.get(endpoint, headers=cls.headers, timeout=20)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Erro ao acessar a API: {e}") from e
        
        dados = response.json()
        if tipo not in dados:
            raise Exception(f"A resposta da API não contém a chave '{tipo}'")
        return dados[tipo]