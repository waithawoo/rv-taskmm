import logging
from typing import Union, Optional
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from src.schemas import PaginationParams, CursorPaginationParams
from src.exceptions import ValidationException
from src.utils import encode_cursor, decode_cursor

from src.helpers.serializer import serialize_model
from src.helpers.response import ApiResponser
from src.helpers.router import route_method, register_routers

from src.modules.auth.dependencies import (
    RoleChecker,
    get_current_user,
    access_token_handler
)

from .services import TaskService
from . import schemas

logger = logging.getLogger(__name__)


class OtherParams(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[int] = None


class TaskRoute:
    def __init__(self):
        self.router = APIRouter()
        self.service = TaskService()
        register_routers(self.router, self)
        self.middlewares = [
            (access_token_handler, ['*']),
            (RoleChecker(['ADMIN']), [('', 'POST'), ('/{id}', 'DELETE')]),
        ]
    
    @property
    def base(self):
        return {
            'router' : self.router,
            'prefix' : 'tasks',
            'middlewares' : self.middlewares
        }

    @route_method(methods=['GET'], route_path='/', response_model=list[schemas.TaskResponseModel])
    async def list(self, request: Request, params: CursorPaginationParams = Depends(), other_params: OtherParams = Depends()):
        try:
            db_session = request.state.db
            decoded_cursor = None
            if params.cursor:
                decoded_cursor = decode_cursor(params.cursor)
            data = await self.service.paginateList(
                db_session,
                cursor=decoded_cursor,
                limit=params.limit,
                status=other_params.status,
                priority=other_params.priority,
                assignee_id=other_params.assignee_id,
                search=params.search,
                sort=params.sort
            )
            data = serialize_model(data, schemas.TaskResponseModel)
            return ApiResponser.success_response(data=data, paginated=True)
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong', 500)
    
    @route_method(methods=['GET'], route_path='/{id}', response_model=schemas.TaskResponseModel)
    async def find(self, request: Request, id: Union[int, str]) -> schemas.TaskResponseModel:
        try: 
            db_session = request.state.db
            data = await self.service.find(db_session, id)
            if data == None:
                return ApiResponser.error_response('No task data found!', 404)
            data = serialize_model(data, schemas.TaskResponseModel)
            return ApiResponser.success_response(data=data)
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong', 500)

    @route_method(methods=['POST'], route_path='/', response_model=schemas.TaskResponseModel)
    async def create(self, request: Request, data: schemas.TaskCreateModel, user = Depends(get_current_user)):
        try:
            db_session = request.state.db
            result = await self.service.create(db_session, data, user)
            result = serialize_model(result, schemas.TaskResponseModel)
            return ApiResponser.success_response(data=result)
        except ValidationException as e:
            logger.error(str(e))
            raise e
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500)
        
    @route_method(methods=['PATCH'], route_path='/{id}', response_model=schemas.TaskResponseModel)
    async def update(self, request: Request, data: schemas.TaskUpdateModel, id: Union[int, str], user = Depends(get_current_user)):
        try:
            db_session = request.state.db
            if user.role != 'ADMIN':
                existing_task = await self.service.find(db_session, id)
                if existing_task == None:
                    return ApiResponser.error_response('No task data found!', 404)
                if existing_task.assignee_id != user.id:
                    return ApiResponser.error_response('You are not authorized to update this task!', 403)
                else:
                    data.title = existing_task.title
                    data.description = existing_task.description
                    data.priority = existing_task.priority
                    data.due_date = existing_task.due_date
                    data.assignee_id = existing_task.assignee_id
            result = await self.service.update(db_session, id, data)
            if result == None:
                return ApiResponser.error_response('No task data found!', 404)
            result = serialize_model(result, schemas.TaskResponseModel)
            return ApiResponser.success_response(data=result)
        except ValidationException as e:
            logger.error(str(e))
            raise e
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500)

    @route_method(methods=['DELETE'], route_path='/{id}')
    async def delete(self, request: Request, id: Union[int, str]):
        try:
            db_session = request.state.db
            result = await self.service.delete(db_session, id)
            if result == False :
                return ApiResponser.error_response('No task data found!', 404)
            return ApiResponser.success_response(data=[])
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500)
