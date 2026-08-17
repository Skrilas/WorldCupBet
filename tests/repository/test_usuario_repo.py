import pytest

from src.repository.usuario_repository import UsuarioRepository

def test_listar_por_palpites(usuario, session):
    repo = UsuarioRepository(session)

    usuario1 = usuario(2,1)
    usuario2 = usuario(2,0)
    usuario3 = usuario(1,2)
    usuario4 = usuario(1,1)
    usuario5 = usuario(1,0)

    session.add(usuario1)
    session.add(usuario2)
    session.add(usuario3)
    session.add(usuario4)
    session.add(usuario5)

    session.commit()

    resultado = repo.listar_por_palpites()

    assert resultado == [usuario1, usuario2, usuario3, usuario4, usuario5]