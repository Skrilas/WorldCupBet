from sqlmodel import create_engine, Session
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): #Classe para pegar a URL do banco pelo .env
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

#conexão com o banco de dados

engine = create_engine(settings.database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session