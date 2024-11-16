"""Settings module for the database"""
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    """Settings for the database"""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PG_USERNAME: str = Field(...)
    PG_PASSWORD: str = Field(...)
    PG_HOST: str = Field(...)
    PG_PORT: int = Field(...)
    PG_DATABASE: str = Field(...)
    PG_SSL: bool = Field(default=False)


class AuthSettings(BaseSettings):
    """Settings for the database"""

    ACCESS_TOKEN_EXPIRES_IN_DAYS: int = Field(default=7)
    REFRESH_TOKEN_EXPIRES_IN_WEEKS: int = Field(default=4)
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_SECRET: str = Field(...)

    SESSION_SECRET_KEY: str = Field(...)

    GOOGLE_CLIENT_ID: str = Field(...)
    GOOGLE_CLIENT_SECRET: str = Field(...)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GeneralSettings(BaseSettings):
    """Settings for the database"""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENV: str = Field(...)


class PaymentSettings(BaseSettings):
    """Settings for the payment"""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    STRIPE_SECRET_KEY: str = Field(...)
    STRIPE_PUBLISHABLE_KEY: str = Field(...)
    STRIPE_WEBHOOK_SECRET: str = Field(...)


@lru_cache()
def get_general_settings():
    """Return the general settings object, run only once"""
    return GeneralSettings()


@lru_cache()
def get_db_settings():
    """Return the database settings object, run only once"""
    return DBSettings()


@lru_cache()
def get_auth_settings():
    """Return the auth settings object, run only once"""
    return AuthSettings()


@lru_cache()
def get_payment_settings():
    """Return the payment settings object, run only once"""
    return PaymentSettings()
