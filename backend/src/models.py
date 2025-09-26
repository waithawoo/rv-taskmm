import uuid
import inspect
from datetime import datetime
from typing import List
from sqlalchemy.orm import DeclarativeBase
from decimal import Decimal


class Base(DeclarativeBase):

    def as_dict(self, included: List[str] = [], excluded: List[str] = []):
        result = {}
        sensitive_fields = getattr(self, '__sensitive_fields__', set())
        
        for c in self.__table__.columns:
            if c.name in sensitive_fields or c.name in excluded:
                continue
            if len(included) > 0 and c.name not in included:
                continue
            value = getattr(self, c.name)
            if isinstance(value, uuid.UUID):
                result[c.name] = str(value)
            elif isinstance(value, datetime):
                result[c.name] = value.isoformat()
            elif isinstance(value, Decimal):
                result[c.name] = float(value)
            else:
                result[c.name] = value
        
        for name, method in inspect.getmembers(self.__class__, predicate=lambda m: isinstance(m, property)):
            if name in excluded:
                continue

            if included and name not in included:
                continue

            result[name] = getattr(self, name)
            
        return result
