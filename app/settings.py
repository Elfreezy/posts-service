from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

CURRENT_FOLDER = Path(__file__).parent.resolve()
ENV_FILE_PATH = CURRENT_FOLDER / ".env"


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_HOST: str
    REDIS_PORT: str
    CACHE_TTL: int
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore")


settings = Settings()
