from uuid import UUID

from sqlalchemy import select, insert, update, delete

from models import Service_Name
from db.postgres import database


class ServiceCrud:
    @staticmethod
    async def create(service_name:str) -> UUID:
        query = insert(Service_Name).values(
            name=service_name,
        )
        return await database.execute(query)

    @staticmethod
    async def update(service_uuid:UUID, service_name:str) -> UUID:
        query = update(Service_Name).where(
            Service_Name.uuid == service_uuid).values(
            name=service_name,
        )
        return await database.execute(query)

    @staticmethod
    async def delete(service_uuid:UUID) -> None:
        query = delete(Service_Name).where(
            Service_Name.uuid == service_uuid
        )
        return await database.execute(query)

    @staticmethod
    async def get_by_uuid(service_uuid:UUID) -> Service_Name:
        query = select(Service_Name).where(
            Service_Name.uuid == service_uuid
        )
        return await database.fetch_one(query)

    @staticmethod
    async def get_by_name(service_name:str) -> Service_Name:
        query = select(Service_Name).where(
            Service_Name.name == service_name
        )
        return await database.fetch_one(query)