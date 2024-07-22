from typing import Optional

class RedisConnectionError(ConnectionError):
    def __init__(self, url: str, message: Optional[str] = None,):
        base_message = f"Error: Failed to connect to redis at {url}"
        message = f"Details: {message}"
        final_message = f"{base_message}\n{message}"
        super().__init__(final_message)

class RedisSessionCreationError(Exception):
    def __init__(self, url: str, message: Optional[str] = None):
        base_message = f"Error: Failed to create a redis session at {url}"
        message = f"Details: {message}"
        final_message = f"{base_message}\n{message}"
        super().__init__(final_message)
