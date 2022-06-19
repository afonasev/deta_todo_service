# noqa:N805
from functools import cache

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    # Common settings
    PROJECT_NAME: str = 'Deta Todo Service'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    # WPS323 - Found `%` string formatting
    LOGGING_FORMAT: str = (
        '%(asctime)s %(levelname)s %(name)s %(message)s'  # noqa:WPS323
    )
    LOGGING_LEVEL: str = 'INFO'

    @validator('*', pre=True)
    def empty_str_to_none(cls, input_value):  # noqa:N805
        if input_value == '':
            return None
        return input_value

    class Config:
        env_prefix = ''


@cache
def get_settings() -> Settings:
    return Settings()
