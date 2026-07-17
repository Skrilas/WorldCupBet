from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    api_url: str = Field(alias="API_URL")
    historico_api_url: str = Field(alias="HISTORICO_API_URL")
    historico_api_key: str = Field(alias="HISTORICO_API_KEY")

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()