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

    @property
    def get_url(self) -> str:
        return self.url or f"redis://{self.host}:{self.port}/{self.db}"
