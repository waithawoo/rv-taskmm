import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, func, text, delete, not_, asc, desc, or_
from sqlalchemy.orm import Query, undefer, joinedload, selectinload, load_only
from sqlalchemy.exc import IntegrityError

from src.exceptions import ValidationException
from src.helpers.paginator import Paginator, CursorPaginator

logger = logging.getLogger(__name__)


class RepositoryError(Exception):
    pass


class BaseRepository:
    def __init__(self, model):
        self.model = model

    def _apply_eager_loading(self, query: Query, relationships: Optional[List[dict]] = []):
        """
        Automatically apply eager loading options (e.g., selectinload) to the query.
        """
        if len(relationships) > 0:
            for rel in relationships:
                relationship_name = rel.get('relation')
                columns = rel.get('columns', [])

                # Dynamically resolve the relationship attribute
                relationship_attr = getattr(self.model, relationship_name, None)
                if not relationship_attr:
                    raise AttributeError(f'Model "{self.model.__name__}" has no attribute "{relationship_name}"')

                if columns:
                    # Dynamically resolve the columns for the related model
                    column_attrs = [getattr(relationship_attr.property.mapper.class_, col) for col in columns]
                    query = query.options(selectinload(relationship_attr).load_only(*column_attrs))
                else:
                    query = query.options(selectinload(relationship_attr))
        return query
    
    def _get_valid_attributes(self, attributes):
        valid_attributes = {}

        valid_columns = self.model.__mapper__.columns.keys()
        
        for key, value in attributes.items():
            if key in valid_columns or key == 'password':
                valid_attributes[key] = value

        return valid_attributes

    async def get_by_raw_sql(self, session: AsyncSession, sql: str, params: Optional[dict] = None):
        try:
            result = await session.execute(text(sql), params or {})
            return result.mappings().all()
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed to execute raw SQL in {self.model.__name__}') from e
    
    async def paginate_by_raw_sql(self, session: AsyncSession, sql: str, params: Optional[dict] = None, page: int = 1, per_page: int = 10):
        try:
            params = params or {}

            count_sql = f'SELECT COUNT(*) FROM ({sql.split('ORDER BY')[0]}) AS total_count'
            count_result = await session.execute(text(count_sql), params)
            total_count = count_result.scalar()

            paginated_sql = f'{sql} LIMIT :limit OFFSET :offset'
            params.update({'limit': per_page, 'offset': (page - 1) * per_page})

            result = await session.execute(text(paginated_sql), params)
            data = result.mappings().all()
            
            return Paginator(data, total_count, page, per_page)
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed to execute raw SQL in {self.model.__name__}') from e

    async def get_all(self, session: AsyncSession, relationships: Optional[List[dict]] = []):
        try:
            statement = select(self.model).filter(self.model.deleted_at == None)
            statement = self._apply_eager_loading(statement, relationships)

            result = await session.execute(statement)
            items = result.scalars().unique().all()

            return items
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e

    async def paginate_cursor(
        self,
        session: AsyncSession,
        cursor: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        conditions: dict = {},
        relationships: Optional[List[dict]] = [],
        search: Optional[str] = None,
        search_columns: Optional[List[str]] = None,
        sort: Optional[str] = None,
    ):
        try:
            filters = [self.model.deleted_at == None]

            # Conditions filters
            for column, value in conditions.items():
                if hasattr(self.model, column):
                    column_attribute = getattr(self.model, column)
                    if isinstance(value, list):
                        filters.append(column_attribute.in_(value))
                    else:
                        filters.append(column_attribute == value)

            # Search filters
            if search and search_columns:
                search_filters = []
                for col_name in search_columns:
                    if hasattr(self.model, col_name):
                        column_attr = getattr(self.model, col_name)
                        search_filters.append(column_attr.ilike(f'%{search}%'))
                if search_filters:
                    filters.append(or_(*search_filters))

            statement = select(self.model).where(and_(*filters))

            # Sorting
            sort_column = 'id'
            order_direction = desc
            if sort:
                if sort.startswith('-'):
                    sort_column = sort[1:]
                    order_direction = desc
                else:
                    sort_column = sort
                    order_direction = asc

            if hasattr(self.model, sort_column):
                statement = statement.order_by(order_direction(getattr(self.model, sort_column)))
            else:
                statement = statement.order_by(desc(self.model.id))

            # Cursor filter
            if cursor and 'last_id' in cursor:
                last_id = cursor['last_id']
                sort_key = cursor.get('sort', sort_column)
                if hasattr(self.model, sort_key):
                    column_attr = getattr(self.model, sort_key)
                    if order_direction == asc:
                        statement = statement.where(column_attr > last_id)
                    else:
                        statement = statement.where(column_attr < last_id)

            statement = statement.limit(limit + 1) # limit + 1 isto check hasNext
            statement = self._apply_eager_loading(statement, relationships)

            result = await session.execute(statement)
            items = result.scalars().unique().all()

            has_next = len(items) > limit
            if has_next:
                items = items[:-1]

            next_cursor = None
            if has_next and items:
                last_item = items[-1]
                next_cursor = {
                    'last_id': getattr(last_item, sort_column),
                    'sort': sort_column,
                }
            return CursorPaginator(items, limit, has_next, next_cursor)
        except Exception as e:
            logger.error(f'Cursor pagination failed in {self.model.__name__}: {str(e)}')
            raise RepositoryError(f'Cursor pagination failed in {self.model.__name__}') from e
        
    async def paginate(self, session: AsyncSession, page: int = 1, per_page: int = 10, conditions: dict = {}, relationships: Optional[List[dict]] = []):
        try:
            filters = [self.model.deleted_at == None]

            for column, value in conditions.items():
                column_attribute = getattr(self.model, column)
                filters.append(column_attribute == value)
            
            total = await session.execute(select(func.count()).select_from(self.model).where(and_(*filters)))
            total = total.scalar()

            offset = (page - 1) * per_page
            # statement = select(self.model).filter(self.model.deleted_at == None).offset(offset).limit(per_page)
            statement = select(self.model).where(and_(*filters)).offset(offset).limit(per_page)
            statement = self._apply_eager_loading(statement, relationships)

            result = await session.execute(statement)
            items = result.scalars().unique().all()
            
            return Paginator(items, total, page, per_page)
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Pagination failed in {self.model.__name__}') from e

    async def get_by_id(self, session: AsyncSession, id, relationships: Optional[List[dict]] = [], load_sensitive: bool = False):
        try:
            # Add undefer option if sensitive fields need to be loaded
            # Currently need only for password_hash
            options = []
            if load_sensitive and hasattr(self.model, 'password_hash'):
                options.append(undefer(self.model.password_hash))
                
            statement = select(self.model).filter(self.model.id == id).filter(self.model.deleted_at == None)
            statement = self._apply_eager_loading(statement, relationships)
            result = await session.execute(statement)
            
            return result.scalars().first()
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e

    async def where_first(self, session: AsyncSession, conditions: dict = {}, relationships: Optional[List[dict]] = [], load_sensitive: bool = False):
        try:
            filters = []
            for column, value in conditions.items():
                column_attribute = getattr(self.model, column)
                filters.append(column_attribute == value)

            # Add undefer option if sensitive fields need to be loaded
            # Currently need only for password_hash
            options = []
            if load_sensitive and hasattr(self.model, 'password_hash'):
                options.append(undefer(self.model.password_hash))
            
            filters.append(self.model.deleted_at == None)  # Exclude soft-deleted records
            
            statement = select(self.model).options(*options).where(and_(*filters))
            statement = self._apply_eager_loading(statement, relationships)
            
            result = await session.execute(statement)
            return result.scalars().first()
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e

    async def where_all(self, session: AsyncSession, conditions: dict = {}, relationships: Optional[List[dict]] = [], load_sensitive: bool = False):
        try:
            filters = []
            for column, value in conditions.items():
                column_attribute = getattr(self.model, column)
                filters.append(column_attribute == value)

            # Add undefer option if sensitive fields need to be loaded
            # Currently need only for password_hash
            options = []
            if load_sensitive and hasattr(self.model, 'password_hash'):
                options.append(undefer(self.model.password_hash))
                
            filters.append(self.model.deleted_at == None)  # Exclude soft-deleted records
            
            statement = select(self.model).where(and_(*filters))
            statement = self._apply_eager_loading(statement, relationships)
            
            result = await session.execute(statement)
            return result.scalars().all()
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e

    async def create(self, session: AsyncSession, attributes: dict):
        try:
            valid_attributes = self._get_valid_attributes(attributes)
            entity = self.model(**valid_attributes)
            session.add(entity)
            await session.commit()
            await session.refresh(entity)
            return entity
        except IntegrityError as e:
            logger.error(f'{str(e)}')
            code, error = e.orig.args
            if str(code) == '1062':  # MySQL error code for duplicate entry
                column = error.split('key')[-1]
                validation_error_details = {
                    'validationErrors': {
                        'field': column, 
                        'error': f'{column} already existed.'
                        }
                }
                raise ValidationException(details=validation_error_details)
            raise RepositoryError(f'Failed in {self.model.__name__}') from e
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e

    async def update(self, session: AsyncSession, id, attributes: dict):
        try:
            entity = await session.get(self.model, id)
            if entity:
                valid_attributes = self._get_valid_attributes(attributes)
                for key, value in valid_attributes.items():
                    setattr(entity, key, value)
                await session.commit()
                await session.refresh(entity)
                return entity
            return None
        except IntegrityError as e:
            logger.error(f'{str(e)}')
            # Handle different database error formats
            if hasattr(e, 'orig') and e.orig.args:
                if len(e.orig.args) >= 2:
                    code, error = e.orig.args[:2]
                    if str(code) == '1062':  # MySQL error code for duplicate entry
                        column = error.split('key')[-1]
                        validation_error_details = {
                            'validationErrors': {
                                'field': column, 
                                'error': f'{column} already existed.'
                                }
                        }
                        raise ValidationException(details=validation_error_details)
            raise RepositoryError(f'Failed in {self.model.__name__}') from e
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e
    
    async def update_where_first(self, session: AsyncSession, where_conditions, attributes: dict):
        try:
            conditions = [getattr(self.model, key) == value for key, value in where_conditions.items()]

            query = select(self.model).where(*conditions)
            result = await session.execute(query)
            entity = result.scalars().first()
            if entity:
                valid_attributes = self._get_valid_attributes(attributes)
                for key, value in valid_attributes.items():
                    setattr(entity, key, value)
                await session.commit()
                await session.refresh(entity)
                return entity
            return None
        except IntegrityError as e:
            logger.error(f'{str(e)}')
            code, error = e.orig.args
            if str(code) == '1062':  # MySQL error code for duplicate entry
                column = error.split('key')[-1]
                validation_error_details = {
                    'validationErrors': {
                        'field': column, 
                        'error': f'{column} already existed.'
                    }
                }
                raise ValidationException(details=validation_error_details)
            raise RepositoryError(f'Failed in {self.model.__name__}') from e
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e
        
    async def update_where_all(self, session: AsyncSession, where_conditions, attributes: dict):
        try:
            conditions = [getattr(self.model, key) == value for key, value in where_conditions.items()]
            
            query = select(self.model).where(*conditions)
            result = await session.execute(query)
            entities = result.scalars().all()

            if entities:
                valid_attributes = self._get_valid_attributes(attributes)
                for entity in entities:
                    for key, value in valid_attributes.items():
                        setattr(entity, key, value)
                await session.commit()
                for entity in entities:
                    await session.refresh(entity)
                return entities
            return None
        except IntegrityError as e:
            logger.error(f'{str(e)}')
            code, error = e.orig.args
            if str(code) == '1062':  # MySQL error code for duplicate entry
                column = error.split('key')[-1]
                validation_error_details = {
                    'validationErrors': {
                        'field': column, 
                        'error': f'{column} already existed.'
                    }
                }
                raise ValidationException(details=validation_error_details)
            raise RepositoryError(f'Failed in {self.model.__name__}') from e
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e

    async def delete(self, session: AsyncSession, id):
        try:
            entity = await session.get(self.model, id)
            if entity:
                await session.delete(entity)
                await session.commit()
                return True
            return False
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e

    async def delete_where(self, session: AsyncSession, where_conditions: dict):
        try:
            conditions = [getattr(self.model, key) == value for key, value in where_conditions.items()]
            stmt = delete(self.model).where(and_(*conditions))
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e
            
    async def delete_where_not(self, session: AsyncSession, where_conditions: dict):
        try:
            conditions = [not_(getattr(self.model, key) == value) for key, value in where_conditions.items()]
            stmt = delete(self.model).where(and_(*conditions))
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount
        except Exception as e:
            logger.error(f'{str(e)}')
            raise RepositoryError(f'Failed in {self.model.__name__}') from e
