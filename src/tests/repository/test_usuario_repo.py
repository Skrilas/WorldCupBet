import pytest

from repository.usuario_repository import UsuarioRepository

def test_salvar(usuario, session):
    repo = UsuarioRepository(session)

    repo.salvar(usuario)

    session.commit()

    resultado = repo.buscar_por_id(usuario.id)

    assert resultado is not None