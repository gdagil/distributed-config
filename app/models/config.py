from sqlalchemy import Column, text, String, TIMESTAMP, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from db.postgres import Base


class Config_Name(Base):
    uuid = Column(UUID(), primary_key=True, server_default=text("uuid_generate_v4()"), unique=True, index=True)
    name = Column(String, unique=False, nullable=False)
    last_value_uuid = Column(UUID(), ForeignKey("config_value.uuid", ondelete="CASCADE"), unique=True, nullable=False)
    service_uuid = Column(UUID(), ForeignKey("service_name.uuid", ondelete="CASCADE"), unique=False, nullable=False)

    datetime_create = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.now())
    datetime_update = Column(TIMESTAMP(timezone=False), nullable=False, onupdate=func.now(), server_default=func.now())

    config_value = relationship("Config_Value", back_populates="config_name")
    service_name = relationship("Service_Name", back_populates="config_name")

    
class Config_Value(Base):
    uuid = Column(UUID(), primary_key=True, server_default=text("uuid_generate_v4()"), unique=True, index=True)
    value = Column(String, unique=False, nullable=False)
    version = Column(Integer, unique=False, nullable=False, server_default=text("1"))
    prev_value_uuid = Column(UUID(), unique=True, nullable=True)

    datetime_create = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.now())
    datetime_update = Column(TIMESTAMP(timezone=False), nullable=False, onupdate=func.now(), server_default=func.now())

    config_name = relationship("Config_Name", back_populates="config_value", cascade="all, delete", passive_deletes=True, uselist=False) # 1 к 1