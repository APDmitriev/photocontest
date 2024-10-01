from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return URL.create('postgresql+asyncpg',
                          username=self.DB_USER,
                          password=self.DB_PASS,
                          host=self.DB_HOST,
                          port=self.DB_PORT,
                          database=self.DB_NAME)

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)


settings = DbSettings()
