import redis
from django.conf import settings

pool = redis.ConnectionPool(
    host=settings.REDIS_CONFIG["host"],
    port=settings.REDIS_CONFIG["port"],
    db=settings.REDIS_CONFIG["db"],
    max_connections=settings.REDIS_CONFIG["max_connections"],
)

# Create a Redis client that uses the pool
redis_client = redis.Redis(connection_pool=pool)
