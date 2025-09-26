from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, field_validator

from src.schemas import CustomValidator
from src.schemas import validate_foreign_exitence
from src.modules.user.models import User


class TaskResponseModel(BaseModel):
    id: Union[int, str]
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]
    assignee_id: Optional[Union[int, str]]
    creator_id: Union[int, str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


required_field_lists = ['title', 'status', 'priority']


class TaskCreateModel(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    due_date: Optional[datetime] = None
    assignee_id: Optional[Union[int, str]] = None
    
    @field_validator(*required_field_lists)
    def validate_fields(value, info):
        return CustomValidator.required_fields(value, info.field_name)

    async def validate_foreign_ids(self, db_session):
        id_model_pair = [
            {
                'column_name': 'assignee_id',
                'id_value': self.assignee_id,
                'model': User
            },
        ]
        await validate_foreign_exitence(db_session, id_model_pair)
        return self
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'title': 'Task Title',
                'description': 'Task Description',
                'status': 'TODO',
                'priority': 'MEDIUM',
                'due_date': '2024-12-31T23:59:59',
                'assignee_id': None,
                'creator_id': 1
            }
        },
    )


class TaskUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[Union[int, str]] = None
    
    @field_validator(*required_field_lists)
    def validate_fields(value, info):
        return CustomValidator.required_fields(value, info.field_name)

    async def validate_foreign_ids(self, db_session):
        id_model_pair = [
            {
                'column_name': 'assignee_id',
                'id_value': self.assignee_id,
                'model': User
            },
            {
                'column_name': 'creator_id',
                'id_value': self.creator_id,
                'model': User
            },
        ]
        await validate_foreign_exitence(db_session, id_model_pair)
        return self
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'title': 'Updated Task Title',
                'description': 'Updated Task Description',
                'status': 'IN_PROGRESS',
                'priority': 'HIGH',
                'due_date': '2024-12-31T23:59:59',
                'assignee_id': 1,
                'creator_id': 1
            }
        },
    )
