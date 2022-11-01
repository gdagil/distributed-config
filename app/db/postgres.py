import databases
from typing import Any
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from core.config import settings as s


DATABASE_URL = f"postgresql+asyncpg://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@{s.POSTGRES_HOST}:{s.POSTGRES_PORT}/{s.POSTGRES_NAME}"


database = databases.Database(DATABASE_URL)
engine = create_async_engine(DATABASE_URL)

@as_declarative()
class Base:
    uuid: Any
    __name__: str
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()