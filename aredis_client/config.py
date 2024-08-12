import json
from typing import Optional

from decouple import config
from pydantic import BaseModel, Field


class RedisConfig(BaseModel):
    host: str = Field(default_factory=lambda: config("REDIS_HOST", "localhost"))
    port: int = Field(default_factory=lambda: int(config("REDIS_PORT", 6379)))
    db: int = Field(default_factory=lambda: int(config("REDIS_DB", 0)))
    password: Optional[str] = Field(default_factory=lambda: config("REDIS_PASSWORD", None))
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
        if self.url:
            return self.url
        else:
            if self.password:
                return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
            return f"redis://{self.host}:{self.port}/{self.db}"
