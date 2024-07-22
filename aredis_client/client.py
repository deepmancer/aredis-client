import contextlib
import threading
import asyncio
import redis.asyncio as redis
from typing import Dict, Optional
from pydantic import BaseModel, Field

from .exceptions import RedisConnectionError, RedisSessionCreationError
from .config import RedisConfig

class AsyncRedis:
    _instances: Dict[str, 'AsyncRedis'] = {}
    _locks: Dict[str, threading.Lock] = {}

    def __new__(cls, config: RedisConfig, *args, **kwargs) -> 'AsyncRedis':
        url = config.get_url()
        if url not in cls._locks:
            cls._locks[url] = threading.Lock()
        with cls._locks[url]:
            if url not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[url] = instance
            return cls._instances[url]

    def __init__(self, config: RedisConfig) -> None:
        if not hasattr(self, 'initialized'):
            self._config = config
            self._redis_client: Optional[redis.Redis] = None
            self.initialized = True

    @staticmethod
    async def create(
        config: Optional[RedisConfig] = None,
        url: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        db: Optional[int] = None,
        **kwargs,
    ) -> 'AsyncRedis':
        if config is None:
            config = RedisConfig(
                url=url,
                host=host,
                port=port,
                db=db,
                **kwargs
            )
        redis_client = AsyncRedis(config)
        await redis_client.connect()
        return redis_client

    @property
    def url(self) -> str:
        return self._config.get_url()

    @contextlib.asynccontextmanager
    async def get_or_create_session(self) -> redis.Redis:
        await self.init()
        try:
            yield self._redis_client
        except Exception as e:
            raise RedisSessionCreationError(url=self.url) from e

    async def connect(self) -> None:
        await self.init()
        try:
            await self._redis_client.ping()
        except Exception as e:
            raise RedisConnectionError(url=self.url, message=str(e))

    async def disconnect(self) -> None:
        if self._redis_client:
            await self._redis_client.close()
            self._redis_client = None

    async def init(self) -> None:
        if self._redis_client is None:
            self._redis_client = self._create_redis_client()

    def _create_redis_client(self) -> redis.Redis:
        return redis.Redis.from_url(self.url, decode_responses=True)
