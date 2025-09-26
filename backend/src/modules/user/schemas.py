from datetime import datetime
from typing import Optional, Literal, Union
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator

from src.schemas import CustomValidator


class UserResponseModel(BaseModel):
    id: Union[int, str]
    name: Optional[str] = None
    email: str
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


required_field_lists = ['email', 'role']


class UserCreateModel(BaseModel):
    name: Optional[str] = Field(max_length=25)
    email: EmailStr = Field(max_length=40)
    role: Literal['USER', 'ADMIN'] = 'USER'
    
    @field_validator(*required_field_lists)
    def validate_fields(value, info):
        return CustomValidator.required_fields(value, info.field_name)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'name': 'user',
                'email': 'user1@gmail.com',
                'role': 'USER',
            }
        },
    )


class UserUpdateModel(BaseModel):
    name: Optional[str] = Field(max_length=25)
    email: EmailStr = Field(max_length=40)
    role: Literal['USER', 'ADMIN'] = 'USER'

    @field_validator(*required_field_lists)
    def validate_fields(value, info):
        return CustomValidator.required_fields(value, info.field_name)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'name': 'user',
                'email': 'user1@gmail.com',
                'role': 'USER',
            }
        },
    )
