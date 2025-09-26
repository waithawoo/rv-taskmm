import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Enum,
    Text,
    ForeignKey,
    TIMESTAMP,
    DECIMAL,
    CHAR,
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship, deferred

from src.models import Base


class {ModelName}(Base):
    __tablename__ = '{module_name}s'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now, nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
