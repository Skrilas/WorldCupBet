from sqlmodel import create_engine, Session
from src.config.settings import settings

#conexão com o banco de dados

engine = create_engine(settings.database_url, echo=True)

def get_session():
    """Fornece uma sessão do banco de dados para a aplicação."""
    with Session(engine) as session:
        yield session