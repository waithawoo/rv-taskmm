import logging
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user.repositories import UserRepository
from . import schemas
from .utils import create_jwt_token

logger = logging.getLogger(__name__)

ACCESS_TOKEN_EXPIRY_MIN = 60
REFRESH_TOKEN_EXPIRY_DAY = 7


class AuthService:
    def __init__(self, model=None):
        self.user_repository = UserRepository(model)

    async def authenticate(self, db_session: AsyncSession, email: str, password: str):
        try:
            user = await self.get_user_by_email(db_session, email, load_sensitive=True)
            if user and user.verify_password(password):
                user_data = {'email': user.email, 'user_id': str(user.id)}
                access_token = create_jwt_token(user_data=user_data, expiry=timedelta(minutes=ACCESS_TOKEN_EXPIRY_MIN))
                refresh_token = create_jwt_token(user_data=user_data, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAY), refresh=True)
                
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'email': user.email, 
                    'id': str(user.id),
                    'role': user.role
                }
            return None
        except Exception as e:
            logger.error(str(e))
            raise Exception(str(e))
    
    async def signup(self, db_session: AsyncSession, user_data: schemas.SingupModel):
        try:
            user_data_dict = user_data.model_dump()
            new_user = await self.user_repository.create(db_session, user_data_dict)
            return new_user
        except Exception as e:
            logger.error(str(e))
            await db_session.rollback()
            raise Exception(str(e))
        
    async def get_user_by_email(self, db_session: AsyncSession, email: str, load_sensitive=False):
        try:
            return await self.user_repository.where_first(db_session, {'email': email}, [], load_sensitive)
        except Exception as e:
            logger.error(str(e))
            raise Exception(str(e))

    async def exists(self, db_session: AsyncSession, email):
        try:
            user = await self.get_user_by_email(db_session, email)
            if not user:
                return None
            return user
        except Exception as e:
            logger.error(str(e))
            raise Exception(str(e))
