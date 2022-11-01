from typing import Literal

from fastapi import APIRouter, status, HTTPException

from crud.config import ConfigCrud
from crud.service import ServiceCrud
from schemas.response import RecValue


router = APIRouter()


@router.get("/history", response_model=dict[str, RecValue],
description=
"""
### Получение истории изменения параметров концигурации
(вложенность может стремиться к бесконечности из-за рекуривного вывода)
""")
async def get_config_versions_history(service:str):
    service_db = await ServiceCrud.get_by_name(service)
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service <<{service}>> not found")
    return await ConfigCrud.get_rec_cong_by_service_uuid(service_db.uuid)


@router.get("", response_model=dict[str,str],
description=
"""
### Получение конфигурации в определённом состоянии
(если версия будет больше, чем существет у параметра, то он будет возвращён в последней версии, которую имеет)
""")
async def get_config_state(service:str, version:Literal["last"]|int="last"):
    service_db = await ServiceCrud.get_by_name(service)
    if not service_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Service <<{service}>> not found")
    if version == "last":
        return await ConfigCrud.get_configs(service_db.uuid)
    return await ConfigCrud.get_configs_state(service_db.uuid, version)