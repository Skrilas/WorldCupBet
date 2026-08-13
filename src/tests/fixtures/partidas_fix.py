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
def partida():
    return create_partida(
        id=1,
        api_id=1
    )


@pytest.fixture
def partida_vencedor_home():
    return create_partida(
        id=6,
        api_id=6,
        data_hora=datetime(2026,1,1),
        terminou=True,
        aposta_ativa= True,

        vencedor_id=758
    )