from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    api_jogos_url: str = Field(alias="API_JOGOS_URL")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()