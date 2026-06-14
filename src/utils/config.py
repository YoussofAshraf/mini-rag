from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables.
    
    Stores API configuration, file upload constraints, and authentication keys
    using Pydantic's BaseSettings for environment variable validation and type safety.
    """
    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    class Config:
        env_file = ".env"


def get_settings():
    """Retrieve and cache the application Settings object.

    Args:
        None

    Returns:
        Settings: Application configuration object with values from environment variables.
    """
    return Settings()
