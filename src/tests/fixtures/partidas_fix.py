import pytest
from datetime import datetime

from models.partida import Partida

def create_partida(**kwargs) -> Partida:
    dados = {
        "home_team_id": 758,
        "away_team_id": 759,
        "data_hora": datetime(2026, 8, 10),
        "vencedor_id": None,
    }
    dados.update(kwargs)
    return Partida(**dados)

@pytest.fixture
def partida_aposta_false():
    return create_partida(
        id=1,
        api_id=1,
        data_hora=datetime(2026,8,22),
        terminou=False,

        aposta_ativa= False
    )

@pytest.fixture
def partida_aposta_funciona():
    return create_partida(
        id=2,
        api_id=2,
        data_hora=datetime(2026,12,22),
        terminou=False,

        aposta_ativa= True
    )

@pytest.fixture
def partida_acontecendo():
    return create_partida(
        id=3,
        api_id=3,
        data_hora=datetime.now(),
        terminou=False,

        aposta_ativa= True
    )

@pytest.fixture
def partida_terminada():
    return create_partida(
        id=4,
        api_id=4,
        data_hora=datetime(2026,1,1),
        terminou=True,

        aposta_ativa= True
    )

@pytest.fixture
def partida_vencedor_home():
    return create_partida(
        id=6,
        api_id=6,
        data_hora=datetime(2026,1,1),
        terminou=True,
        aposta_ativa= True,

        vencedor_id=1
    )

@pytest.fixture
def partida_vencedor_away():
    return create_partida(
        id=7,
        api_id=7,
        data_hora=datetime(2026,1,1),
        terminou=True,
        aposta_ativa= True,

        vencedor_id=2
    )

@pytest.fixture
def partida_empate():
    return create_partida(
        id=8,
        api_id=8,
        data_hora=datetime(2026,1,1),
        terminou=True,
        aposta_ativa= True,

        vencedor_id=None
    )