from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Deta Todo Service'

    # WPS323 - Found `%` string formatting
    LOGGING_FORMAT: str = (
        '%(asctime)s %(levelname)s %(name)s %(message)s'  # noqa:WPS323
    )
    LOGGING_LEVEL: str = 'INFO'

    DETA_PROJECT_KEY: str

    @validator('*', pre=True)
    def empty_str_to_none(cls, input_value):  # noqa:N805
        if input_value == '':
            return None
        return input_value

    class Config:
        env_prefix = ''


settings = Settings()
