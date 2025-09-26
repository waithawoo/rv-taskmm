import logging
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ValidationException

from .repositories import UserRepository
from .schemas import UserCreateModel, UserUpdateModel
from .models import User

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, model=User):
        self._repository = UserRepository(model)

    async def list(self, db_session: AsyncSession):
        try:
            data = await self._repository.get_all(db_session)
            return data
        except Exception as e:
            logger.error(str(e))
            raise Exception(str(e))
        
    async def paginateList(self, db_session: AsyncSession, page, per_page):
        try:
            data = await self._repository.paginate(db_session, page, per_page)
            return data
        except Exception as e:
            logger.error(str(e))
            raise Exception(str(e))
        
    async def find(self, db_session: AsyncSession, id):
        try:
            data = await self._repository.get_by_id(db_session, id)
            return data
        except Exception as e:
            logger.error(str(e))
            raise Exception(str(e))
        
    async def create(self, db_session: AsyncSession, data: UserCreateModel):
        try:
            data_dict = data.model_dump()
            data_dict['password'] = 'password@default'
            result = await self._repository.create(db_session, data_dict)
            return result
        except ValidationException as e:
            logger.error(str(e))
            raise e
        except Exception as e:
            logger.error(str(e))
            await db_session.rollback()
            raise Exception(e)
        
    async def update(self, db_session: AsyncSession, id: Union[int, str], data: UserUpdateModel):
        try:
            data_dict = data.model_dump()
            data = await self._repository.update(db_session, id, data_dict)
            return data
        except ValidationException as e:
            logger.error(str(e))
            raise e
        except Exception as e:
            logger.error(str(e))
            await db_session.rollback()
            raise Exception(str(e))
        
    async def delete(self, db_session: AsyncSession, id: Union[int, str]):
        try:
            result = await self._repository.delete(db_session, id)
            return result
        except Exception as e:
            logger.error(str(e))
            await db_session.rollback()
            raise Exception(str(e))
