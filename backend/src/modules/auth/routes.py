import logging
from datetime import datetime
from fastapi import APIRouter, Depends, Request

from src.helpers.response import ApiResponser
from src.helpers.router import route_method, register_routers
from src.helpers.serializer import serialize_model
from src.db.redis import TokenBlocklist
from src.modules.auth import schemas
from src.modules.user.models import User

from .exceptions import (
    InvalidToken,
)
from .services import AuthService
from .utils import (
    create_jwt_token,
)
from .dependencies import (
    RoleChecker,
    get_current_user,
)
from .dependencies import access_token_handler, refresh_token_handler

logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRY_MIN = 60
REFRESH_TOKEN_EXPIRY_DAY = 7


class AuthRoute:
    def __init__(self):
        self.router = APIRouter()
        self.service = AuthService(User)
        register_routers(self.router, self)
        self.middlewares = [
            (access_token_handler, ['/profile', '/logout']),
        ]
        self.token_blocklist = TokenBlocklist()

    @property
    def base(self):
        return {
            'router': self.router,
            'prefix': 'auth',
            'middlewares': self.middlewares
        }
    
    @route_method(methods=['GET'], route_path='/profile')
    async def profile(self, request: Request, user = Depends(get_current_user)):
        try:
            return ApiResponser.success_response(data=user)
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500)

    @route_method(methods=['POST'], route_path='/signup', response_model=schemas.SignupResponseModel)
    async def signup(self, request: Request, user_data: schemas.SingupModel):
        try:
            db_session = request.state.db
            email = user_data.email
            user_exists = await self.service.exists(db_session, email)
            if user_exists:
                return ApiResponser.error_response('User with email already exists', 400)
            new_user = await self.service.signup(db_session, user_data)
            new_user = serialize_model(new_user, schemas.SignupResponseModel)
            return ApiResponser.success_response(data=new_user)
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500)

    @route_method(methods=['POST'])
    async def login(self, request: Request, login_data: schemas.LoginModel):
        try:
            db_session = request.state.db
            user = await self.service.authenticate(db_session, login_data.email, login_data.password)
            if user:
                return ApiResponser.success_response(user)
            return ApiResponser.error_response('Invalid Email or Password', 403)
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500)

    @route_method(methods=['GET'], route_path='/logout')
    async def logout(self, token_details: dict = access_token_handler):
        jti = token_details['jti']
        await self.token_blocklist.block_token(jti)
        return ApiResponser.success_response(message='Logged Out Successfully')
    
    @route_method(methods=['GET'], route_path='/refresh_token')
    async def refresh_token(self, request: Request, token_details: dict = refresh_token_handler):
        try:
            expiry_timestamp = token_details['exp']
            if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
                new_access_token = create_jwt_token(user_data=token_details['user'])
                return ApiResponser.success_response({'access_token': new_access_token})
            raise InvalidToken
        except Exception as e:
            logger.error(str(e))
            return ApiResponser.error_response('Something went wrong!', 500)
