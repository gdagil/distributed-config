from sqlalchemy import Column, text, String, TIMESTAMP, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from db.postgres import Base


class Service_Name(Base):
    uuid = Column(UUID(), primary_key=True, server_default=text("uuid_generate_v4()"), unique=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    datetime_create = Column(TIMESTAMP(timezone=False), nullable=False, server_default=func.now())
    datetime_update = Column(TIMESTAMP(timezone=False), nullable=False, onupdate=func.now(), server_default=func.now())

    config_name = relationship("Config_Name", back_populates="service_name", cascade="all, delete", passive_deletes=True, uselist=True)