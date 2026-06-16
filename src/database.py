from sqlmodel import create_engine, Session
from config.settings import settings

#conexão com o banco de dados

engine = create_engine(settings.database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session