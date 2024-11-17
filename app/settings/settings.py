"""Settings module for the database"""
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralSettings(BaseSettings):
    """Settings for the database"""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENV: str = Field(...)

@lru_cache()
def get_general_settings():
    """Return the general settings object, run only once"""
    return GeneralSettings()
