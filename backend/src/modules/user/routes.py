import logging
from typing import Union
from fastapi import APIRouter, Depends, Request

from src.schemas import PaginationParams
from src.exceptions import ValidationException
from src.helpers.serializer import serialize_model
from src.helpers.response import ApiResponser
from src.helpers.router import route_method, register_routers

from src.modules.auth.dependencies import (
    RoleChecker,
    get_current_user,
    access_token_handler
)
from .services import UserService
from . import schemas

logger = logging.getLogger(__name__)


class UserRoute:
    def __init__(self):
        self.router = APIRouter()
        self.service = UserService()
        register_routers(self.router, self)
        self.middlewares = [
            (RoleChecker(['ADMIN']), ['/create', '/update/{id}', '/delete/{id}', '/find/{id}']),
        ]
    
    @property
    def base(self):
        return {
            'router' : self.router,
            'prefix' : 'users',
            'middlewares' : self.middlewares
        }

    @route_method(methods=['GET'], response_model=list[schemas.UserResponseModel])
    async def list(self, request: Request, params: PaginationParams = Depends()):
        try:
            db_session = request.state.db
            if params.page is None or params.per_page is None:
                data = await self.service.list(db_session)
            else:
                data = await self.service.paginateList(db_session, params.page, params.per_page)
            data = serialize_model(data, schemas.UserResponseModel)
            return ApiResponser.success_response(data=data, paginated=True)
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong', 500)
    
    @route_method(methods=['GET'],route_path='/find/{id}', response_model=schemas.UserResponseModel)
    async def find(self, request: Request, id: Union[int, str]) -> schemas.UserResponseModel:
        try: 
            db_session = request.state.db
            data = await self.service.find(db_session, id)
            if data == None:
                return ApiResponser.error_response('No user data found!', 404)
            data = serialize_model(data, schemas.UserResponseModel)
            return ApiResponser.success_response(data=data)
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong', 500)

    @route_method(methods=['POST'], response_model=schemas.UserResponseModel)
    async def create(self, request: Request, data: schemas.UserCreateModel):
        try:
            db_session = request.state.db
            result = await self.service.create(db_session, data)
            result = serialize_model(result, schemas.UserResponseModel)
            return ApiResponser.success_response(data=result)
        except ValidationException as e:
            logger.error(str(e))
            raise e
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500)
        
    @route_method(methods=['POST'], route_path='/update/{id}', response_model=schemas.UserResponseModel)
    async def update(self, request: Request, data: schemas.UserUpdateModel, id: Union[int, str]):
        try:
            db_session = request.state.db
            result = await self.service.update(db_session, id, data)

            if result == None:
                return ApiResponser.error_response('No user data found!', 404)
            result = serialize_model(result, schemas.UserResponseModel)
            return ApiResponser.success_response(data=result)
        except ValidationException as e:
            logger.error(str(e))
            raise e
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500)

    @route_method(methods=['DELETE'],route_path='/delete/{id}')
    async def delete(self, request: Request, id: Union[int, str]):
        try:
            db_session = request.state.db
            result = await self.service.delete(db_session, id)
            if result == False :
                return ApiResponser.error_response('No user data found!', 404)
            return ApiResponser.success_response(data=[])
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500)
