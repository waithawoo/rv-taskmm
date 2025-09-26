import logging
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ValidationException

from .repositories import TaskRepository
from . import schemas
from .models import Task

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, model=Task):
        self._repository = TaskRepository(model)

    async def list(self, db_session: AsyncSession):
        try:
            data = await self._repository.get_all(db_session)
            return data
        except Exception as e:
            logger.error(str(e))
            raise Exception(str(e))
    
    async def paginateList(
        self,
        session: AsyncSession,
        cursor: str | None = None,
        limit: int = 10,
        status: str = None,
        priority: str = None,
        assignee_id: int = None,
        search: str = None,
        sort: str = None
    ):
        try:
            conditions = {}
            if status:
                conditions['status'] = status
            if priority:
                conditions['priority'] = priority
            if assignee_id:
                conditions['assignee_id'] = assignee_id
                
            search_columns = ['title', 'description']

            result = await self._repository.paginate_cursor(
                session=session,
                cursor=cursor,
                limit=limit,
                conditions=conditions,
                search=search,
                search_columns=search_columns,
                sort=sort
            )

            return result
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

    async def create(self, db_session: AsyncSession, data: schemas.TaskCreateModel, user):
        try:
            data_dict = data.model_dump()
            data_dict['creator_id'] = user.id
            result = await self._repository.create(db_session, data_dict)
            return result
        except ValidationException as e:
            logger.error(str(e))
            raise e
        except Exception as e:
            logger.error(str(e))
            await db_session.rollback()
            raise Exception(e)
        
    async def update(self, db_session: AsyncSession, id: Union[int, str], data: schemas.TaskUpdateModel):
        try:
            data_dict = data.model_dump(exclude_none=True)
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
