from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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
    
    model_config = SettingsConfigDict(env_file=".env")



settings = Settings() # type: ignore 

DB_URL_asyncpg = settings.DATABASE_URL_asyncpg
BOT_TOKEN = settings.BOT_TOKEN
CRYPTOBOT_API_TOKEN = settings.CRYPTOBOT_API_TOKEN