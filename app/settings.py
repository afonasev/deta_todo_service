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

    # Application specific settings
    DETA_PROJECT_KEY: str

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(
        cls, addresses: str | list[str]  # noqa:N805
    ) -> list[str] | str:
        if not isinstance(addresses, str):
            return addresses
        if not addresses.startswith('['):
            return [address.strip() for address in addresses.split(',')]
        return addresses

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
