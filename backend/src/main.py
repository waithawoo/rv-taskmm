import logging
import logging.config
import yaml
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.exceptions import register_exceptions
from src.middlewares import register_global_middlewares
from src.helpers.router import register_route_middlewares
from src.routes import routes
from src.db.core import sessionmanager


def load_config(path='settings.yml'):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f'Failed to load config file {path}: {e}')
        raise

config = load_config()

logging.config.dictConfig(config.get('logging', {}))
logger = logging.getLogger(__name__)

version = 'v1'
description = 'TaskMM REST API'

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Starting up Server...')
    try:
        await sessionmanager.initialize()
        logger.info('Database session manager initialized')
        logger.info('Server startup complete!')
        yield
    finally:
        logger.info('Shutting down Server...')
        try:
            await sessionmanager.close()
            logger.info('All database connections closed')
        except Exception as e:
            logger.error(f'Error during shutdown: {e}')
        
        logger.info('Server shutdown complete!')


app = FastAPI(
    title='TaskMM',
    description=description,
    version=version,
    docs_url='/doc/api-doc',
    redoc_url='/doc/api-redoc',
    openapi_url='/doc/openapi.json',
    lifespan=lifespan
)

register_exceptions(app)
register_global_middlewares(app)
register_route_middlewares(routes)

for router in routes:
    app.include_router(
        router['router'],
        prefix=f'/api/{version}/{router['prefix']}',
        tags=[router['prefix'].capitalize()],
    )
