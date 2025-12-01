import redis.asyncio as redis
from core.config import settings

redis_client = None

async def get_redis():
    global redis_client
    if redis_client is None:
        try:
            redis_url = settings.REDIS_URL
            if redis_url:
                redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
                # Test connection
                await redis_client.ping()
            else:
                print("Warning: REDIS_URL not set. Caching disabled.")
        except Exception as e:
            print(f"Warning: Could not connect to Redis: {e}. Caching disabled.")
            redis_client = None
    return redis_client
