from time import time
from src.db.redis import RedisClient

RATE_LIMIT = 50
RATE_LIMIT_TIME_WINDOW = 60


class RateLimiter:
    def __init__(self, redis: RedisClient, rate_limit=RATE_LIMIT, expiry=RATE_LIMIT_TIME_WINDOW):
        self.redis = redis
        self.rate_limit = rate_limit
        self.expiry = expiry

    @classmethod
    async def create(cls, redis_client=None):
        redis_client = redis_client or RedisClient()
        redis = await redis_client.connect()
        return cls(redis)
    
    async def is_rate_limited(self, ip: str):
        current_time = int(time())
        async with self.redis.pipeline() as pipe:
            key = f'rate-limit:{ip}'
            pipe.zadd(key, {str(current_time): current_time})
            pipe.zremrangebyscore(key, 0, current_time - self.expiry)
            pipe.zcard(key)
            pipe.expire(key, self.expiry)
            _, _, request_count, _ = await pipe.execute()
            
            if request_count > self.rate_limit:
                return True
            return False
