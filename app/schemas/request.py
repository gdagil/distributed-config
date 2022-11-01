from pydantic import BaseModel, validator


class CreateConfig(BaseModel):
    service: str
    data: list[dict[str,str]]

    @validator("data")
    def validate_data(cls, v):
        list_of_un_keys = list()
        for value in v:
            key = next(iter(value))
            if len(value.keys()) != 1:
                raise ValueError('Each dictionary should have only one key')
            if key in list_of_un_keys:
                raise ValueError(f'Found duplicate keys <<{key}>>')
            list_of_un_keys.append(key)
        return v

    class Config:
        schema_extra = {
            "example": {
                "service": "managed-k8s",
                "data": [
                    {"key1": "value1"},
                    {"key2": "value2"}
                ]
            }
        }

class UpdateConfigs(CreateConfig):
    pass


