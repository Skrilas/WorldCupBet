import pytest

from repository.apostas_repository import ApostasRepository
from repository.usuario_repository import UsuarioRepository
from repository.partida_repository import PartidaRepository
from schemas.estatistica_aposta import EstatisticaAposta
from repository.time_repository import TimeRepository
from enums.status_aposta import StatusAposta

@pytest.mark.parametrize(
        "status, resultado",
        [
            (StatusAposta.PENDENTE, True),
            (StatusAposta.PERDEU, False)
        ]
)
def test_usu_aposta_pendente(time_um, time_dois, partida, usuario, aposta, session, status, resultado):
    time_repo = TimeRepository(session)
    part_repo = PartidaRepository(session)
    ap_repo = ApostasRepository(session)
    usu_repo = UsuarioRepository(session)

    usu = usuario()
    apost = aposta()

    usu.id = 1
    apost.usuario_id = 1
    apost.status = status
    time_repo.salvar(time_um)
    time_repo.salvar(time_dois)
    usu_repo.salvar(usu)
    session.flush()
    part_repo.salvar(partida)
    session.flush()
    ap_repo.salvar(apost)
    session.commit()

    assert ap_repo.possui_apostas_pendentes(usu.id) == resultado


@pytest.mark.parametrize(
        "total_apostadores, resposta",
        [
        (0, []),
        (1, [EstatisticaAposta(
            time_id=758,
            total_apostadores=1,
            total_pontos=100
        )]),
        (2, [EstatisticaAposta(
            time_id=758,
            total_apostadores=2,
            total_pontos=200
        )])
        ]
)
def test_obter_estatistica(session, total_apostadores, resposta, usuario, aposta, time_um, time_dois, partida):
    time_repo = TimeRepository(session)
    part_repo = PartidaRepository(session)
    ap_repo = ApostasRepository(session)
    usu_repo = UsuarioRepository(session)

    time_repo.salvar(time_um)
    time_repo.salvar(time_dois)
    session.flush()

    part_repo.salvar(partida)
    session.flush()

    for i in range(total_apostadores):
        usu = usuario()

        usu_repo.salvar(usu)
        session.flush()

        apost = aposta(
            usuario_id=usu.id,
            partida_id=partida.id,
            time_id=time_um.id,
            qtd_pontos=100
        )

        ap_repo.salvar(apost)

    session.commit()

    assert ap_repo.obter_estatisticas_aposta(partida.id) == resposta