import pytest

from sqlmodel import Session
from database import engine

@pytest.fixture
def session():
    with Session(engine) as session:
        yield session