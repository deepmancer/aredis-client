import asyncio
import contextlib
from typing import Dict, Optional, AsyncIterator

import redis.asyncio as aioredis

from .config import RedisConfig
from .exceptions import RedisConnectionError, RedisSessionCreationError


class AsyncRedis:
    _instances: Dict[str, 'AsyncRedis'] = {}
    _locks: Dict[str, asyncio.Lock] = {}

    def __new__(cls, config: RedisConfig, *args, **kwargs) -> 'AsyncRedis':
        url: str = config.get_url()
        if url not in cls._locks:
            cls._locks[url] = asyncio.Lock()
        if url not in cls._instances:
            cls._instances[url] = super().__new__(cls)
        return cls._instances[url]

    def __init__(self, config: RedisConfig) -> None:
        if not hasattr(self, '_initialized') or not self._initialized:
            self._config: RedisConfig = config
            self._redis_client: Optional[aioredis.Redis] = None
            self._initialized: bool = True

    @classmethod
    async def create(cls, config: Optional[RedisConfig] = None, **kwargs) -> 'AsyncRedis':
        if config is None:
            config = RedisConfig(**kwargs)
        url: str = config.get_url()
        if url not in cls._locks:
            cls._locks[url] = asyncio.Lock()
        async with cls._locks[url]:
            if url not in cls._instances:
                instance = cls(config)
                await instance.connect()
                cls._instances[url] = instance
        return cls._instances[url]

    async def connect(self) -> None:
        if self._redis_client is None:
            try:
                self._redis_client = aioredis.Redis(
                    host=self._config.host,
                    port=self._config.port,
                    db=self._config.db,
                    password=self._config.password,
                    decode_responses=True,
                    health_check_interval=30,
                )
                await self._redis_client.ping()
            except Exception as e:
                raise RedisConnectionError(url=self.url, message=str(e))

    async def disconnect(self) -> None:
        if self._redis_client:
            await self._redis_client.close()
            self._redis_client = None

    @contextlib.asynccontextmanager
    async def get_or_create_session(self) -> AsyncIterator[aioredis.Redis]:
        await self.connect()
        try:
            yield self._redis_client
        except Exception as e:
            raise RedisSessionCreationError(url=self.url, message=str(e))

    async def reconnect(self) -> None:
        await self.disconnect()
        await self.connect()

    @property
    def url(self) -> str:
        return self._config.get_url()
