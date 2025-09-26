from typing import Union, Optional
from fastapi import Query
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from sqlalchemy.future import select

from src.exceptions import ValidationException


class CustomValidator:
    
    @classmethod
    def required_fields(self, value: str, field_name: str) -> str:
        if not value or (isinstance(value, str) and value.strip() == ''):
            raise ValueError(f'{field_name} must not be empty')
        return value


class PaginationParams(BaseModel):
    page: Union[int, None] = Query(default=None, description='Page number (1-based index).')
    per_page: Union[int, None] = Query(default=None, le=100, description='Number of items per page (max 100).')
    search: Optional[str] = None
    sort: Optional[str] = None


class CursorPaginationParams(BaseModel):
    cursor: Optional[str] = Field(None, description='Opaque cursor token from previous page')
    limit: int = Field(10, ge=1, le=100, description='Number of items to fetch per request')
    search: Optional[str] = None
    sort: Optional[str] = None


async def validate_foreign_exitence(db_session, id_model_pair:list[dict]):    
    for each in id_model_pair:
        result = await db_session.execute(select(each['model']).filter_by(id=each['id_value']))
        data = result.scalars().first()
        if not data:
            validation_error_details = {
                'validationErrors': {
                    'field': f'{each['column_name']}', 
                    'error': f'{each['column_name']} not found'
                    }
            }
            raise ValidationException(details=validation_error_details)
