from datetime import timedelta
from pydantic import BaseSettings

# Базовая конфигурация сервиса
class Settings(BaseSettings):
    BACK_END_DOMAIN_ORIGIN:str
    FRONT_END_DOMAIN_ORIGIN:str

    POSTGRES_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_NAME: str 
    POSTGRES_HOST: str

    class Config:
        env_file = "./.env.dev"

settings = Settings()