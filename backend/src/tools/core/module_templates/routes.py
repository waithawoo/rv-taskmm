import logging
from typing import Union

from fastapi import APIRouter, Depends, status, Request

from src.config import Config
from src.schemas import PaginationParams
from src.exceptions import ValidationException

from src.helpers.serializer import serialize_model
from src.helpers.response import ApiResponser
from src.helpers.router import route_method, register_routers
from src.helpers.i18n import _

from src.modules.auth.dependencies import (
    RoleChecker,
    get_current_user,
    access_token_handler
)

from .models import {ModelName}
from .services import {ModelName}Service
from . import schemas

logger = logging.getLogger(__name__)


class {ModelName}Route:
    def __init__(self):
        self.router = APIRouter()
        self.service = {ModelName}Service({ModelName})
        register_routers(self.router, self)
        self.middlewares = []
    
    @property
    def base(self):
        return {
            'router' : self.router,
            'prefix' : '{module_name}s',
            'middlewares' : self.middlewares
        }

    @route_method(methods=['GET'], response_model=list[schemas.{ModelName}ResponseModel])
    async def list(self, request: Request, params: PaginationParams = Depends()):
        try:
            db_session = request.state.db
            if params.page is None or params.per_page is None:
                data = await self.service.list(db_session)
            else:
                data = await self.service.paginateList(db_session, params.page, params.per_page)
            data = serialize_model(data, schemas.{ModelName}ResponseModel)
            return ApiResponser.success_response(data=data, paginated=True)
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong', 500, str(e))
    
    @route_method(methods=['GET'],route_path='/find/{id}', response_model=schemas.{ModelName}ResponseModel)
    async def find(self, request: Request, id: Union[int, str]) -> schemas.{ModelName}ResponseModel:
        try: 
            db_session = request.state.db
            data = await self.service.find(db_session, id)
            if data == None:
                return ApiResponser.error_response('No {module_name} data found!', 404)
            data = serialize_model(data, schemas.{ModelName}ResponseModel)
            return ApiResponser.success_response(data=data)
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong', 500, str(e))

    @route_method(methods=['POST'], response_model=schemas.{ModelName}ResponseModel)
    async def create(self, request: Request, data: schemas.{ModelName}CreateModel):
        try:
            db_session = request.state.db
            result = await self.service.create(db_session, data)
            result = serialize_model(result, schemas.{ModelName}ResponseModel)
            return ApiResponser.success_response(data=result, message=_('http_success'))
        except ValidationException as e:
            logger.error(str(e))
            raise e
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500, str(e))
        
    @route_method(methods=['POST'], route_path='/update/{id}', response_model=schemas.{ModelName}ResponseModel)
    async def update(self, request: Request, data: schemas.{ModelName}UpdateModel, id: Union[int, str]):
        try:
            db_session = request.state.db
            result = await self.service.update(db_session, id, data)
            if result == None:
                return ApiResponser.error_response('No {module_name} data found!', 404)
            result = serialize_model(result, schemas.{ModelName}ResponseModel)
            return ApiResponser.success_response(data=result, message=_('http_success'))
        except ValidationException as e:
            logger.error(str(e))
            raise e
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500, str(e))

    @route_method(methods=['DELETE'],route_path='/delete/{id}')
    async def delete(self, request: Request, id: Union[int, str]):
        try:
            db_session = request.state.db
            result = await self.service.delete(db_session, id)
            if result == False :
                return ApiResponser.error_response('No {module_name} data found!', 404)
            return ApiResponser.success_response(data=[], message=_('http_success'))
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500, str(e))
