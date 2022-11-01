from uuid import UUID

from sqlalchemy import select, insert, update, delete

from models import Config_Name, Config_Value
from db.postgres import database


class ConfigCrud:
    @staticmethod
    async def create_configs(configs:list[dict[str,str]], service_uuid:UUID) -> None:
        for config in configs:
            name = next(iter(config))
            value_uuid = await ConfigCrud.create_config_value(config[name])
            await ConfigCrud.create_config_name(name, value_uuid, service_uuid)

    @staticmethod
    async def create_config_name(name:str, value_uuid:UUID, service_uuid:UUID) -> UUID:
        query = insert(Config_Name).values(
            name=name,
            service_uuid=service_uuid,
            last_value_uuid=value_uuid
        )
        return await database.execute(query)

    @staticmethod
    async def create_config_value(value:str) -> UUID:
        query = insert(Config_Value).values(
            value=value,
            version=1
        )
        return await database.execute(query)

    @staticmethod
    async def get_configs(service_uuid:UUID):
        query = select(Config_Name.name, Config_Value.value).where(
            Config_Name.service_uuid == service_uuid,
            Config_Value.uuid==Config_Name.last_value_uuid
            )
        return dict([(row.name, row.value) for row in await database.fetch_all(query)])

    @staticmethod
    async def get_configs_state(service_uuid:UUID, need_version:int):
        return dict([
            (
                conf.name, 
                (await ConfigCrud.get_config_value_state(
                    conf.last_value_uuid,
                    need_version
                )).value
            )
            for conf in await ConfigCrud.get_all_configs_names(service_uuid)]
        )

    @staticmethod
    async def get_config_value_state(conf_value_uuid:UUID, need_version:int) -> Config_Value:
        config_value = await database.fetch_one(
                select(Config_Value).where(
                Config_Value.uuid==conf_value_uuid
            )
        )
        if config_value.version > need_version and config_value.prev_value_uuid:
            return await ConfigCrud.get_config_value_state(config_value.prev_value_uuid, need_version)
        return config_value


    @staticmethod
    async def get_config_by_name_and_service_uuid(config_name:str, service_uuid:UUID) -> Config_Name:
        query = select(Config_Name).where(
            Config_Name.name == config_name,
            Config_Name.service_uuid == service_uuid
        )
        return await database.fetch_one(query)

    @staticmethod
    async def get_config_value(conf_value_uuid:UUID) -> Config_Value:
        query = select(Config_Value).where(
            Config_Value.uuid == conf_value_uuid
        )
        return await database.fetch_one(query)

    @staticmethod
    async def update_config(new_config:dict[str,str], prev_conf:Config_Name, last_version:int):
        query_conf_value = insert(Config_Value).values(
            value=new_config[next(iter(new_config))],
            prev_value_uuid=prev_conf.last_value_uuid,
            version=last_version+1
        )
        new_value_uuid = await database.execute(query_conf_value)
        query_cinf_name = update(Config_Name).where(
            Config_Name.uuid == prev_conf.uuid).values(
                last_value_uuid=new_value_uuid
            )
        return await database.execute(query_cinf_name)
        
    @staticmethod
    async def recursion_get_config_versions(conf_value_uuid:UUID):
        config_value = await ConfigCrud.get_config_value(conf_value_uuid)
        resp_dict = dict(config_value)
        if config_value.prev_value_uuid:
            resp_dict.setdefault("prev_version",
            await ConfigCrud.recursion_get_config_versions(config_value.prev_value_uuid))
        return resp_dict

    @staticmethod
    async def recursion_delete_conf_values(conf_value_uuid:UUID):
        config_value = await ConfigCrud.get_config_value(conf_value_uuid)
        if config_value.prev_value_uuid:
            await ConfigCrud.recursion_delete_conf_values(config_value.prev_value_uuid)
        return await database.execute(
            delete(Config_Value).where(
                Config_Value.uuid == config_value.uuid
                )
            )

    @staticmethod
    async def get_all_configs_names(service_uuid:UUID) -> list[Config_Name]:
        query = select(Config_Name).where(
            Config_Name.service_uuid==service_uuid
        )
        return await database.fetch_all(query)

    @staticmethod
    async def get_rec_cong_by_service_uuid(service_uuid:UUID):
        return dict([(conf.name, 
            dict(
                await ConfigCrud.recursion_get_config_versions(conf.last_value_uuid)
                )
            ) 
        for conf in await ConfigCrud.get_all_configs_names(service_uuid)])

    @staticmethod
    async def delete_configs_values_by_service_uuid(service_uuid:UUID) -> None:
        conf_names = await ConfigCrud.get_all_configs_names(service_uuid)
        for conf in conf_names:
            await ConfigCrud.recursion_delete_conf_values(conf.last_value_uuid)

