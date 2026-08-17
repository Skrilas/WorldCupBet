from decimal import Decimal
import pytest

from src.models.apostas import Apostas

def create_aposta(**kwargs):
    dados = {
        "usuario_id": 1,
        "partida_id": 1,
        "time_id": 758,
        "qtd_pontos": 100,
        "odd": Decimal("1.5")
    }
    dados.update(kwargs)
    return Apostas(**dados)

@pytest.fixture
def aposta():
    def _aposta(**kwargs):
        return create_aposta(**kwargs)
    return _aposta