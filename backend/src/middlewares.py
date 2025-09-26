import time
import logging

from fastapi import FastAPI, HTTPException, Header
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.db.core import sessionmanager
from src.helpers.response import ApiResponser
from src.helpers.ratelimiter import RateLimiter
from src.config import Config

logger = logging.getLogger('uvicorn.access')
logger.disabled = True

logger = logging.getLogger(__name__)


def register_global_middlewares(app: FastAPI):
    """Register global middlewares."""
    
    @app.middleware('http')
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        processing_time = time.time() - start_time
        message = f'{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s'
        logger.info(message)
        return response

    @app.middleware('http')
    async def rate_limiter(request: Request, call_next):
        rate_limiter = await RateLimiter.create()
        client_ip = request.client.host
        if await rate_limiter.is_rate_limited(client_ip):
            return ApiResponser.error_response(message='Too Many Requests', status_code=429)

        response = await call_next(request)
        return response
    
    @app.middleware('http')
    async def db_session_middleware(request: Request, call_next):
        db_session = None
  
        try:
            excluded_routes = ['/api-doc', '/openapi.json', '/doc/api-doc', '/doc/openapi.json']
            if request.url.path in excluded_routes:
                return await call_next(request)

            db_session = await sessionmanager.get_session()

            request.state.db = db_session
            
            response = await call_next(request)
            
            if response.status_code < 400:
                await db_session.commit()
            else:
                await db_session.rollback()
                
            return response
        except HTTPException as e:
            if db_session is not None:
                try:
                    await db_session.rollback()
                except Exception as rollback_error:
                    logger.error(f'Error during rollback: {rollback_error}')
            return ApiResponser.error_response(message=e.detail, status_code=e.status_code)
        except Exception as e:
            if db_session is not None:
                try:
                    await db_session.rollback()
                except Exception as rollback_error:
                    logger.error(f'Error during rollback: {rollback_error}')
            logger.error(f'Database middleware error: {str(e)}', exc_info=True)
            return ApiResponser.error_response(message='Internal Server Error', status_code=500)
        finally:
            if db_session is not None:
                try:
                    await db_session.close()
                    logger.debug('Database session closed successfully')
                except Exception as e:
                    logger.error(f'Error closing database session: {e}')
            
            if hasattr(request.state, 'db'):
                delattr(request.state, 'db')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=Config.cors_allowed_origins,
        allow_methods=Config.cors_allowed_methods,
        allow_headers=Config.cors_allowed_headers,
        allow_credentials=Config.CORS_ALLOW_CREDENTIALS,
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=Config.trusted_hosts,
    )
