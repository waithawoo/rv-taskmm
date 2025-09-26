from redis import asyncio as aioredis
from src.config import Config
from src.exceptions import AppException


class RedisClient:
    def __init__(self, redis_url: str = None):
        self.redis_url = redis_url or Config.REDIS_URL
        self.redis = None

    async def connect(self):
        if not self.redis:
            try:
                self.redis = aioredis.from_url(self.redis_url)
            except Exception as e:
                raise AppException(f'Failed to connect to Redis: {str(e)}')
            return self.redis

    async def set(self, name: str, value: str, expiry: int = None):
        await self.connect()
        try:
            await self.redis.set(name=name, value=value, ex=expiry)
        except Exception as e:
            raise AppException(f'Failed to set key "{name}" in Redis: {str(e)}')

    async def get(self, name: str):
        await self.connect()
        try:
            return await self.redis.get(name)
        except Exception as e:
            raise AppException(f'Failed to get key "{name}" from Redis: {str(e)}')

    async def delete(self, name: str):
        await self.connect()
        try:
            await self.redis.delete(name)
        except Exception as e:
            raise AppException(f'Failed to delete key "{name}" in Redis: {str(e)}')

    async def exists(self, name: str):
        await self.connect()
        try:
            return await self.redis.exists(name) > 0
        except Exception as e:
            raise AppException(f'Failed to check existence of key "{name}" in Redis: {str(e)}')


class TokenBlocklist:
    def __init__(self, redis_client: RedisClient = None, expiry: int = 3600):
        self.redis_client = redis_client or RedisClient()
        self.expiry = expiry

    async def block_token(self, jti: str):
        await self.redis_client.set(name=jti, value='', expiry=self.expiry)

    async def is_token_blocked(self, jti: str) -> bool:
        return await self.redis_client.exists(name=jti)

    async def remove_token(self, jti: str):
        await self.redis_client.delete(name=jti)
