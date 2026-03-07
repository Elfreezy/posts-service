from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

PATH_FOLDER = Path(__file__).parent.resolve()
PATH_ENV_FILE = PATH_FOLDER / ".env"

class TestSettings(BaseSettings):
    TEST_DB_URL: str
    TEST_REDIS_HOST: str
    TEST_REDIS_PORT: int
    TEST_CLIENT_BASE_URL: str

    model_config = SettingsConfigDict(env_file=PATH_ENV_FILE)

test_settings = TestSettings()