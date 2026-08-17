import pytest

from sqlmodel import Session, create_engine, SQLModel
from src.config.settings import settings

from src.models.usuario import Usuario
from src.models.time import Time
from src.models.partida import Partida
from src.models.apostas import Apostas

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