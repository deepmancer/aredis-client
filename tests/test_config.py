import os
import pytest
from decouple import config
from aredis_client.config import RedisConfig

def test_redis_config_default_values():
    # Ensure no environment variables override the defaults
    redis_config = RedisConfig()
    assert redis_config.host == config("REDIS_HOST", "localhost")
    assert redis_config.port == int(config("REDIS_PORT", 6379))
    assert redis_config.db == int(config("REDIS_DB", 0))
    assert redis_config.password == config("REDIS_PASSWORD", None)
    assert redis_config.url is None

def test_redis_config_get_url_without_password():
    redis_config = RedisConfig()
    expected_url = f"redis://{redis_config.host}:{redis_config.port}/{redis_config.db}"
    assert redis_config.get_url() == expected_url

def test_redis_config_get_url_with_password():
    redis_config = RedisConfig(password="my_password")
    expected_url = f"redis://:my_password@{redis_config.host}:{redis_config.port}/{redis_config.db}"
    assert redis_config.get_url() == expected_url

def test_redis_config_with_custom_values():
    # Test with all custom values
    custom_host = "custom_host"
    custom_port = 8888
    custom_db = 1
    custom_password = "custom_password"
    
    redis_config = RedisConfig(
        host=custom_host, 
        port=custom_port, 
        db=custom_db, 
        password=custom_password
    )
    
    assert redis_config.host == custom_host
    assert redis_config.port == custom_port
    assert redis_config.db == custom_db
    assert redis_config.password == custom_password

def test_redis_config_with_url_override():
    # Test if the url is provided directly
    custom_url = "redis://:some_password@some_host:7777/2"
    redis_config = RedisConfig(url=custom_url)
    
    assert redis_config.url == custom_url
    assert redis_config.get_url() == custom_url

def test_redis_config_invalid_port():
    # Test with an invalid port number
    with pytest.raises(ValueError):
        RedisConfig(port="invalid_port")

def test_redis_config_invalid_db():
    # Test with an invalid db value
    with pytest.raises(ValueError):
        RedisConfig(db="invalid_db")

@pytest.mark.parametrize(
    "env_var, env_value, expected_value", 
    [
        ("REDIS_HOST", "env_host", "env_host"),
        ("REDIS_PORT", "9999", 9999),
        ("REDIS_DB", "2", 2),
        ("REDIS_PASSWORD", "env_password", "env_password"),
    ]
)
def test_redis_config_with_environment_variables(monkeypatch, env_var, env_value, expected_value):
    # Test if environment variables are properly picked up
    monkeypatch.setenv(env_var, env_value)
    redis_config = RedisConfig()
    assert getattr(redis_config, env_var.lower().split('_')[1]) == expected_value
