from datetime import datetime
import pytest

from repository.partida_repository import PartidaRepository
from repository.time_repository import TimeRepository


@pytest.mark.parametrize(
        "vencedor_id, nome_vencedor",
        [
            (758, "Time 1"),
            (None, None)
        ]
)
def test_consulta_com_times(partida_vencedor_home, time_um, time_dois, vencedor_id, nome_vencedor, session):
    part_repo = PartidaRepository(session)
    time_repo = TimeRepository(session)

    p1=partida_vencedor_home
    th=time_um
    ta=time_dois
    p1.vencedor_id = vencedor_id

    time_repo.salvar(th)
    time_repo.salvar(ta)
    session.commit()
    part_repo.salvar(p1)
    session.commit()
    result = part_repo.buscar_por_id_com_times(p1.api_id)

    assert result == (p1, th.nome, ta.nome, nome_vencedor)

@pytest.mark.parametrize(
        "aposta_ativa, data_hora, deve_aparecer",
        [
            (True, datetime(2030, 12, 25), True),
            (True, datetime(2026, 1, 1), False),
            (False, datetime(2030, 12, 25), False),
            (False, datetime(2026, 1, 1), False)
        ]
)
def test_mostrar_partidas_ativas(partida, time_um, time_dois, aposta_ativa, data_hora, deve_aparecer, session):
    time_repo = TimeRepository(session)
    partida_repo = PartidaRepository(session)

    time_repo.salvar(time_um)
    time_repo.salvar(time_dois)
    session.commit()

    partida.aposta_ativa = aposta_ativa
    partida.data_hora = data_hora
    partida.vencedor_id = time_um.id

    partida_repo.salvar(partida)
    session.commit()

    result = partida_repo.mostrar_partidas_ativas()

    if deve_aparecer:
        assert result == [(partida, time_um.nome, time_dois.nome, time_um.nome)]
    else:
        assert result == []