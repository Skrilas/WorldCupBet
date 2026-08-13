import pytest

from sqlmodel import Session, create_engine, SQLModel
from config.settings import settings

from models.usuario import Usuario
from models.time import Time
from models.partida import Partida
from models.apostas import Apostas

test_engine = create_engine(settings.test_database_url)

@pytest.fixture
def session(criar_tabelas):
    with Session(test_engine) as session:
        yield session

@pytest.fixture(autouse=True)
def criar_tabelas():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)