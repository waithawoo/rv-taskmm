import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker

from src.config import Config
from src.utils import build_db_url

logging.basicConfig()
logger = logging.getLogger(__name__)


class DatabaseSessionManager:
    """Singleton class to manage async db sessions"""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.engine: AsyncEngine = None 
            self.session_maker: async_sessionmaker = None
            self._initialized = True

    async def initialize(self) -> None:
        if self.engine:
            await self.engine.dispose()

        database_url = build_db_url(
            Config.DB_USER, 
            Config.DB_PASSWORD,
            Config.DB_HOST,
            Config.DB_PORT,
            Config.DB_NAME
        )
        
        self.engine = create_async_engine(
            database_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_timeout=10,
        )
        
        self.session_maker = async_sessionmaker(
            bind=self.engine, 
            class_=AsyncSession, 
            expire_on_commit=False,
        )
    
    async def get_session(self) -> AsyncSession:
        if not self.session_maker:
            raise RuntimeError('Database not initialized. Call initialize() first.')
        return self.session_maker()
            
    async def close(self, tenant: str) -> None:
        if self.engine:
            try:
                await self.engine.dispose()
                logger.info('Database engine disposed')
            except Exception as e:
                logger.error(f'Error disposing engine: {e}')
            finally:
                self.engine = None
                self.session_maker = None
    
    async def health_check(self) -> bool:
        if not self.engine:
            return False

        try:
            async with self.engine.begin() as conn:
                await conn.execute('SELECT 1')
            return True
        except Exception as e:
            logger.warning(f'Health check failed: {e}')
            return False


sessionmanager = DatabaseSessionManager()
