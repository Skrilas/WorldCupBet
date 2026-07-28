from config.hash import password_hasher
from decimal import Decimal
from datetime import date
import pytest

from models.usuario import Usuario

def criar_usuario(**kwargs) -> Usuario:
    dados = {
        "nome": "usuario",
        "email": "usuario@teste.com",
        "cpf": "62722983079",
        "data_nascimento": date(2000, 1, 1),
        "login": "usuario",
        "senha_hash": password_hasher.hash("#Usuario123"),
        "admin": False,
        "pontos": Decimal("100")
    }
    dados.update(kwargs)
    return Usuario(**dados)

@pytest.fixture
def admin():
    return criar_usuario(
        id=1,
        admin=True,
        nome="Admin",
        login="admin",
        email="admin@teste.com"
    )

@pytest.fixture
def usuario():
    return criar_usuario(
        id=2
    )

@pytest.fixture
def usuario_menor_idade():
    return criar_usuario(
        id=3,
        data_nascimento=date(2010, 1, 1)
    )

@pytest.fixture
def usuario_sem_pontos():
    return criar_usuario(
        id=4,
        pontos=Decimal("0")
    )