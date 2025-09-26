from datetime import datetime
from typing import Optional, Literal, Union
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator

from src.schemas import CustomValidator


class SignupResponseModel(BaseModel):
    id: Union[int, str]
    name: Optional[str] = None
    email: str
    role: Literal['USER', 'ADMIN'] = 'USER'
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


required_field_lists = ['email', 'password']


class SingupModel(BaseModel):
    name: Optional[str] = Field(max_length=25)
    email: EmailStr = Field(max_length=40)
    password: str = Field(min_length=6)

    @field_validator(*required_field_lists)
    def validate_fields(value, info):
        return CustomValidator.required_fields(value, info.field_name)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'name': 'John Doe',
                'email': 'johndoe123@gmail.com',
                'password': 'password',
            }
        },
    )


class LoginModel(BaseModel):
    email: EmailStr = Field(max_length=40)
    password: str = Field(min_length=6)
    
    @field_validator(*required_field_lists)
    def validate_fields(value, info):
        return CustomValidator.required_fields(value, info.field_name)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'email': 'johndoe123@gmail.com',
                'password': 'password',
            }
        },
    )
