import pytest
from unittest.mock import AsyncMock, patch, PropertyMock
from aredis_client.client import AsyncRedis
from aredis_client.config import RedisConfig
from aredis_client.exceptions import RedisConnectionError, RedisSessionCreationError

@pytest.mark.asyncio
@patch('aredis_client.client.AsyncRedis.create', new_callable=AsyncMock)
async def test_async_redis_create(mock_create):
    config = RedisConfig(host='localhost', port=6379, db=0, password='password')
    mock_create.return_value = AsyncMock()
    redis = await AsyncRedis.create(config)
    assert redis is not None

@pytest.mark.asyncio
async def test_async_redis_connect():
    config = RedisConfig(host='localhost', port=6379, db=0, password='password')
    redis = AsyncRedis(config)
    redis._redis_client = AsyncMock()
    await redis.connect()
    assert redis._redis_client is not None

@pytest.mark.asyncio
async def test_async_redis_disconnect():
    config = RedisConfig(host='localhost', port=6379, db=0, password='password')
    redis = AsyncRedis(config)
    redis._redis_client = AsyncMock()
    await redis.disconnect()
    assert redis._redis_client is None

@pytest.mark.asyncio
async def test_async_redis_get_or_create_session():
    config = RedisConfig(host='localhost', port=6379, db=0, password='password')
    redis = AsyncRedis(config)
    redis._redis_client = AsyncMock()
    session_mock = AsyncMock()
    with patch.object(redis, 'get_or_create_session', return_value=AsyncMock(__aenter__=AsyncMock(return_value=session_mock), __aexit__=AsyncMock())):
        async with redis.get_or_create_session() as session:
            assert session is not None

@pytest.mark.asyncio
async def test_async_redis_reconnect():
    config = RedisConfig(host='localhost', port=6379, db=0, password='password')
    redis = AsyncRedis(config)

    redis._redis_client = AsyncMock()
    with patch.object(redis, 'connect', new_callable=AsyncMock) as mock_connect, \
        patch.object(redis, 'disconnect', new_callable=AsyncMock) as mock_disconnect:
        
        redis._redis_client.ping = AsyncMock(return_value=True)        
        await redis.reconnect()

        mock_disconnect.assert_awaited_once()
        mock_connect.assert_awaited_once()

        assert redis._redis_client is not None

@pytest.mark.asyncio
async def test_async_redis_url():
    config = RedisConfig(host='localhost', port=6379, db=0, password='password')
    redis = AsyncRedis(config)
    with patch.object(AsyncRedis, 'url', new_callable=PropertyMock) as mock_url:
        mock_url.return_value = 'redis://localhost:6379/0'
        assert redis.url == 'redis://localhost:6379/0'
