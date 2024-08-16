# Async Redis Client

<p align="center">
    <img src="https://img.shields.io/badge/Redis-FF4438.svg?style=for-the-badge&logo=Redis&logoColor=white" alt="Redis">
    <img src="https://img.shields.io/badge/PyPI-3775A9.svg?style=for-the-badge&logo=PyPI&logoColor=white" alt="PyPI">
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
</p>

`aredis-client` is a Python package that provides an asynchronous Redis client using `redis-py`. It offers a singleton-based connection pooling mechanism, ensuring efficient and thread-safe Redis operations.

# Features
- Fully compatible with the `redis-py` library.
- Asynchronous Redis connections using `redis-py`.
- Singleton design pattern to manage Redis connections.
- Context manager support for Redis sessions.
- Easy configuration using `RedisConfig`.

## Installation

To install `aredis-client`, use pip:

```sh
pip install git+https://github.com/deepmancer/aredis-client.git
```

# Usage
Here's a basic example of how to use the AsyncRedis class in your project:

## Configuration
First, create a configuration object using RedisConfig:

```python
from aredis_client import RedisConfig

config = RedisConfig(
    host='localhost',
    port=6379,
    db=0,
)
```
## Creating an AsyncRedis Instance
You can create an instance of AsyncRedis using the configuration:

```python
from aredis_client import AsyncRedis

async def main():
    redis_client = await AsyncRedis.create(config=config)
    print(redis_client.url)
```

## Using Redis Sessions
To interact with the Redis server, use the context manager provided by get_or_create_session:

```python
from aredis_client import AsyncRedis

async def main():
    redis_client = await AsyncRedis.create(config=config)

    async with redis_client.get_or_create_session() as session:
        # Use `session` to interact with your Redis server
        await session.set('key', 'value')
        value = await session.get('key')
        print(value)

    await redis_client.disconnect()
```

## Example Usage
Here's a complete example of how to use aredis-client:

```python
import asyncio
from aredis_client import AsyncRedis, RedisConfig

async def main():
    config = RedisConfig(
        host='localhost',
        port=6379,
        db=0,
    )
    client = await AsyncRedis.create(config=config)

    async with client.get_or_create_session() as session:
        await session.set('key', 'value')
        value = await session.get('key')
        print(f'The value for "key" is {value}')
        
        keys = ['key1', 'key2', 'key3']
        pipeline = session.pipeline()
        for key in keys:
            pipeline.delete(key)
        await pipeline.execute()
        
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## Error Handling
The package provides custom exceptions to handle various Redis-related errors:

- `RedisConnectionError`
- `RedisSessionCreationError`

## Disconnecting
To gracefully disconnect from the Redis server:

```python
await redis_client.disconnect()
```

# License
This project is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/deepmancer/aredis-client/blob/main/LICENSE) file for more details.
