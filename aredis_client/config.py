import json

from typing import Optional, Any, Type, TypeVar, Callable

from decouple import config, UndefinedValueError
from pydantic import BaseModel, Field, ValidationError, validator

T = TypeVar('T')

def env_var(field_name: str, default: Any = None, cast_type: Callable[[str], T] = str) -> T:
    try:
        value = config(field_name, default=default)
        if value is None:
            return default
        return cast_type(value)
    except UndefinedValueError:
        return default
    except (TypeError, ValueError) as e:
        if cast_type is None:
            raise ValueError(f"Failed to cast environment variable {field_name} to {str.__name__}") from e
        else:
            raise ValueError(f"Failed to cast environment variable {field_name} to {cast_type.__name__}") from e


class RedisConfig(BaseModel):
    host: str = Field(default_factory=lambda: env_var("REDIS_HOST", "localhost", str))
    port: int = Field(default_factory=lambda: env_var("REDIS_PORT", 6379, int))
    db: int = Field(default_factory=lambda: env_var("REDIS_DB", 0, int))
    password: Optional[str] = Field(default_factory=lambda: env_var("REDIS_PASSWORD", None, str))
    url: Optional[str] = Field(default=None)

    def __repr__(self) -> str:
        attributes = self.dict(exclude={"url"})
        url = self.url or self.get_url()
        attributes['url'] = url
        attributes_str = json.dumps(attributes, indent=4)[1:-1]
        return f"{self.__class__.__name__}({attributes_str})"

    def __str__(self) -> str:
        return self.__repr__()

    def get_url(self) -> str:
        return self.url or f"redis://{self.host}:{self.port}/{self.db}"