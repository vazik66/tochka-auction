import json
import typing

from pymemcache.client.base import PooledClient

from app.core.config import settings
from app.cache.serialization import JsonSerde
import functools

from app.utils.logger import logger


def get_memcache_client() -> PooledClient:
    client = PooledClient(
        (settings.MEMCACHED_HOST, settings.MEMCACHED_PORT),
        serde=JsonSerde(),
        max_pool_size=4,
    )
    return client


memcache_client = get_memcache_client()


def cache(expire: int = 0, noreply: bool = False):
    # Hardcoded for get_items func.
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> typing.Any:
            key = f'{func.__name__}_{kwargs.get("skip")}_{kwargs.get("limit")}'
            logger.info(f"key: {key}")

            cached_val = memcache_client.get(key)
            if cached_val:
                return json.loads(cached_val)

            new_val = await func(*args, **kwargs)
            memcache_client.set(
                key=key, value=new_val.json(), expire=expire, noreply=noreply
            )
            if hasattr(new_val, "__root__"):
                return new_val.__root__
            return new_val

        return wrapper

    return decorator
