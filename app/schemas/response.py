from __future__ import annotations
from pydantic import BaseModel


class UserResponse(BaseModel):
    success:bool = False
    detail:str|None = None


class Value(BaseModel):
    value: str
    version: int


class RecValue(Value):
    prev_version: RecValue| None = None