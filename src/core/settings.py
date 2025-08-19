from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path(__file__).resolve().parent.parent.parent
CORE_DIR_PATH = Path(__file__).resolve().parents


class Settings(BaseSettings):
    ADMIN_TG_ID: str
    ADMIN_TG_USERNAME: str
    BOT_TOKEN: str
    CRYPTOBOT_API_TOKEN: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=BASE_PATH / ".env")


settings = Settings()  # type: ignore

DB_URL_asyncpg = settings.DATABASE_URL_asyncpg
ADMIN_TG_ID = settings.ADMIN_TG_ID
ADMIN_TG_USERNAME = settings.ADMIN_TG_USERNAME
BOT_TOKEN = settings.BOT_TOKEN
CRYPTOBOT_API_TOKEN = settings.CRYPTOBOT_API_TOKEN
