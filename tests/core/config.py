from pydantic import BaseSettings

# Конфигурация тестирования
class Settings(BaseSettings):
    TEST_TARGET_HOST: str
    TEST_TARGET_PORT: int

    class Config:
        env_file = "./.env.dev"

settings = Settings()

def get_target():
    return f"{settings.TEST_TARGET_HOST}:{settings.TEST_TARGET_PORT}"