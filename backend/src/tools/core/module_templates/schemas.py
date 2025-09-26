import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Union
from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator, model_validator
from pydantic.functional_serializers import field_serializer

from src.schemas import CustomValidator
from src.schemas import validate_foreign_exitence


class {ModelName}ResponseModel(BaseModel):
    id: Union[int, str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


required_field_lists = []


class {ModelName}CreateModel(BaseModel):

    # Only if `required_field_lists` is not empty, Uncomment this validator code
    # @field_validator(*required_field_lists)
    # def validate_fields(value, info):
    #     return CustomValidator.required_fields(value, info.field_name)

    # This is for validating foreign id check
    # e.g.
    # id_model_pair = [
    #     {
    #         'column_name': 'menu_id',
    #         'id_value': self.menu_id,
    #         'model': Menu
    #     },
    # ]
    # async def validate_foreign_ids(self, db_session):
    #     id_model_pair = []
    #     await validate_foreign_exitence(db_session, id_model_pair)
    #     return self
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {}
        },
    )


class {ModelName}UpdateModel(BaseModel):

    # Only if `required_field_lists` is not empty, Uncomment this validator code
    # @field_validator(*required_field_lists)
    # def validate_fields(value, info):
    #     return CustomValidator.required_fields(value, info.field_name)

    # This is for validating foreign id check
    # e.g.
    # id_model_pair = [
    #     {
    #         'column_name': 'menu_id',
    #         'id_value': self.menu_id,
    #         'model': Menu
    #     },
    # ]
    # async def validate_foreign_ids(self, db_session):
    #     id_model_pair = []
    #     await validate_foreign_exitence(db_session, id_model_pair)
    #     return self
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {}
        },
    )
