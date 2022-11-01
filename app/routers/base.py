from fastapi import APIRouter, status, HTTPException

from crud.config import ConfigCrud
from crud.service import ServiceCrud
from schemas.request import CreateConfig, UpdateConfigs
from schemas.response import UserResponse


router = APIRouter()


@router.get("", response_model=dict[str,str],
description=
"""
### Получение конфигурации последней версии по названию сервиса
"""
)
async def get_config_by_service_name(service:str):
    service_db = await ServiceCrud.get_by_name(service)
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service <<{service}>> not found")
    return await ConfigCrud.get_configs(service_db.uuid)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
description=
"""
### Создание конфигурации
В каждом словаре тредуется указать только одино значение "key": "value"
""")
async def create_config(data:CreateConfig):
    if await ServiceCrud.get_by_name(data.service):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Service already exists")
    service_uuid = await ServiceCrud.create(data.service)
    await ConfigCrud.create_configs(data.data, service_uuid)
    return UserResponse(success=True, detail="Successfully created")


@router.put("", response_model=UserResponse,
description=
"""
### Изменение занчения параметров конфигурации
В каждом словаре тредуется указать только одино значение "key": "value"
""")
async def update_config_by_service_name(data:UpdateConfigs):
    service_db = await ServiceCrud.get_by_name(data.service)
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service <<{data.service}>> not found")
    for config in data.data:
        config_name = next(iter(config))
        config_db = await ConfigCrud.get_config_by_name_and_service_uuid(config_name, service_db.uuid)
        if not config_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Config <<{config_name}>> not found")
        conf_val_db = await ConfigCrud.get_config_value(config_db.last_value_uuid)
        if config[config_name] == conf_val_db.value:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Key <<{config_name}>> already have <<{config[config_name]}>> value")
        await ConfigCrud.update_config(config, config_db, last_version=conf_val_db.version)
    await ServiceCrud.update(service_db.uuid, service_db.name)
    return UserResponse(success=True, detail="Successfully updated")


@router.delete("", response_model=UserResponse,
description=
"""
### Удаление концигурации
""")
async def delete_config_by_service_name(service:str):
    service_db = await ServiceCrud.get_by_name(service)
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service <<{service}>> not found")
    await ConfigCrud.delete_configs_values_by_service_uuid(service_db.uuid)
    await ServiceCrud.delete(service_db.uuid)
    return UserResponse(success=True, detail="Successfully deleted")


