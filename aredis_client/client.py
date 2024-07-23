import contextlib
import asyncio
import redis.asyncio as aioredis
from typing import Dict, Optional
from pydantic import BaseModel

from .exceptions import RedisConnectionError, RedisSessionCreationError
from .config import RedisConfig

class AsyncRedis:
    _instances: Dict[str, 'AsyncRedis'] = {}
    _locks: Dict[str, asyncio.Lock] = {}

    def __new__(cls, config: RedisConfig, *args, **kwargs) -> 'AsyncRedis':
        url = config.get_url()
        if url not in cls._locks:
            cls._locks[url] = asyncio.Lock()
        return cls._instances.get(url, None) or super().__new__(cls)

    def __init__(self, config: RedisConfig) -> None:
        if not hasattr(self, '_initialized') or not self._initialized:
            self._config = config
            self._redis_client: Optional[aioredis.Redis] = None
            self._initialized = True

    @classmethod
    async def create(cls, config: Optional[RedisConfig] = None, **kwargs) -> 'AsyncRedis':
        if config is None:
            config = RedisConfig(**kwargs)
        redis_client = cls(config)
        await redis_client.connect()
        return redis_client

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
    async def get_or_create_session(self) -> aioredis.Redis:
        await self.connect()
        try:
            yield self._redis_client
        except Exception as e:
            raise RedisSessionCreationError(url=self.url) from e

    @property
    def url(self) -> str:
        return self._config.get_url()