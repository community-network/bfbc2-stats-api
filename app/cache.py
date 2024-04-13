import sys
from datetime import timedelta
from typing import Any

import redis.asyncio.client
import redis.asyncio
import redis.asyncio.cluster
import redis

from app.singleton import Singleton
from app import config


class RedisClient(metaclass=Singleton):
    client: redis.asyncio.Redis

    async def redis_connect(self) -> redis.asyncio.client.Redis:
        """Connect to the redis host"""
        try:
            self.client = redis.asyncio.Redis(
                host=str(config.REDIS_HOST),
                port=int(config.REDIS_PORT),
                password=str(config.REDIS_PASS),
                socket_timeout=5,
            )
            ping = await self.client.ping()
            if ping is True:
                return
        except redis.AuthenticationError:
            print("Redis authentication error!")
            sys.exit(1)
        except redis.exceptions.RedisClusterException:
            self.client = redis.asyncio.Redis(
                host=str(config.REDIS_HOST),
                port=int(config.REDIS_PORT),
                password=str(config.REDIS_PASS),
                db=0,
                socket_timeout=5,
            )
            ping = await self.client.ping()
            if ping is True:
                return

    async def get_from_cache(self, key: str) -> Any:
        """Data from redis."""
        val = None
        try:
            val = await self.client.get(key)
        except Exception as e:
            print(f"failed to get cache! {e}")
        return val

    async def set_to_cache(
        self, key: str, value: str, ttl: int = config.CACHE_TTL_DEFAULT
    ) -> bool:
        """Data to redis."""
        try:
            state = await self.client.setex(key, timedelta(seconds=ttl), value=value)
            return state
        except Exception as e:
            print(f"failed to set cache! {e}")

    async def get_multiple_from_cache(self, keys: list[str]) -> Any:
        try:
            prefixed_keys = [config.REDIS_KEY_PREFIX + key for key in keys]
            values = await self.client.mget(prefixed_keys)
            return values
        except Exception as e:
            print(f"failed to get cache! {e}")
            return []

    async def set_multiple_to_cache(
        self, mapping: dict, ttl: int = config.CACHE_TTL_DEFAULT
    ) -> bool:
        try:
            states = []
            for key, value in mapping.items():
                state = await self.set_to_cache(key, value, ttl)
                states.append(state)

            return all(states)
        except Exception as e:
            print(f"failed to set cache! {e}")
