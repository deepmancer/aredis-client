from typing import Optional, Any, Type, TypeVar

from pydantic import BaseModel, Field, ValidationError, validator
from decouple import config, UndefinedValueError

T = TypeVar('T')

def env_var(field_name: str, default = None, cast_type = str) -> T:
    try:
        value = config(field_name, default=default)
        return cast_type(value)
    except Exception:
        return default

class RedisConfig(BaseModel):
    host: Optional[str] = Field(default_factory=lambda: env_var("REDIS_HOST", "localhost", str))
    port: Optional[int] = Field(default_factory=lambda: env_var("REDIS_PORT", 6379, int))
    db: Optional[int] = Field(default_factory=lambda: env_var("REDIS_DB", 0, int))
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
