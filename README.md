# 🧰 Async Redis Client

<p align="center">
    <img src="https://img.shields.io/badge/Redis-FF4438.svg?style=for-the-badge&logo=Redis&logoColor=white" alt="Redis">
    <img src="https://img.shields.io/badge/PyPI-3775A9.svg?style=for-the-badge&logo=PyPI&logoColor=white" alt="PyPI">
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
</p>

**`aredis-client`** is your go-to Python package for seamless asynchronous Redis interactions, powered by `redis-py`. With its singleton-based connection pooling, it ensures efficient, thread-safe operations, making your Redis experience faster and easier.

---

## ✨ Features

- 💼 **Full Compatibility**: Works effortlessly with the `redis-py` library.
- ⚡ **Asynchronous Operations**: Async Redis connections for improved performance.
- 🛠️ **Singleton Pattern**: Efficiently manage Redis connections using a singleton design.
- 🔄 **Context Manager Support**: Easily manage Redis sessions.
- 🔧 **Simple Configuration**: Configure effortlessly with `RedisConfig`.

## 📦 Installation

Get started quickly by installing `aredis-client` with pip:

```sh
pip install git+https://github.com/deepmancer/aredis-client.git
```

## 📝 Usage Guide

### 🔧 Configuration

Start by creating a configuration object with `RedisConfig`:

```python
from aredis_client import RedisConfig

config = RedisConfig(
    host='localhost',
    port=6379,
    db=0,
)
```

### 🏗️ Creating an AsyncRedis Instance

Next, create an instance of `AsyncRedis` using the configuration:

```python
from aredis_client import AsyncRedis

async def main():
    redis_client = await AsyncRedis.create(config=config)
    print(redis_client.url)
```

### ⚙️ Managing Redis Sessions

Interact with the Redis server using the context manager from `get_or_create_session`:

```python
from aredis_client import AsyncRedis

async def main():
    redis_client = await AsyncRedis.create(config=config)

    async with redis_client.get_or_create_session() as session:
        # Interact with your Redis server
        await session.set('key', 'value')
        value = await session.get('key')
        print(value)

    await redis_client.disconnect()
```

### 🔍 Example Usage

Here's a complete example to demonstrate the power of `aredis-client`:

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

### 🛡️ Error Handling

Stay safe with custom exceptions to handle Redis-related errors:

- `RedisConnectionError`
- `RedisSessionCreationError`

### 🛑 Disconnecting

Ensure a clean disconnect from the Redis server:

```python
await redis_client.disconnect()
```

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/deepmancer/aredis-client/blob/main/LICENSE) file for full details.

---

**Get started with `aredis-client` today and take your Redis operations much easier!** 🚀
