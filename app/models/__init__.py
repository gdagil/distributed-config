import asyncio
from .config import Config_Name, Config_Value
from .service import Service_Name
from db.postgres import Base, engine


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())


# Base.metadata.create_all(engine)