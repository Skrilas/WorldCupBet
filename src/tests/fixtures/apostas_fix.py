from decimal import Decimal
import pytest

from models.apostas import Apostas

def create_aposta(**kwargs):
    dados = {
        "id": 1,
        "usuario_id": 1,
        "partida_id": 1,
        "time_id": 1,
        "qtd_pontos": 100,
        "odd": Decimal("1.5")
    }
    dados.update(kwargs)
    return Apostas(**dados)

@pytest.fixture
def aposta():
    return create_aposta()