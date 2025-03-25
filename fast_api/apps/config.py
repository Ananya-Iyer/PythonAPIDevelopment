# from pydantic import BaseSettings # pydantic v1
from pydantic_settings import BaseSettings # pydantic v2 BaseSettings mved to pydantic-settings


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str # set to str because port is in url so its always in str and never int
    DATABASE_NAME: str
    DATABASE_USERNAME: str = "postgres"
    DATABASE_PASSWORD: str = "localhost"
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
