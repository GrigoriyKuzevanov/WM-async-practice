import os
from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database settings
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    ECHO_SQL: bool
    POOL_SIZE: int = 20
    MAX_OVERFLOW: int = 10

    @computed_field
    @property
    def asyncpg_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    NAMING_CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    # Alembic configuration
    SCRIPT_LOCATION: str = "parser/migration_utils/alembic"
    VERSION_LOCATIONS: str = ""
    FILE_TEMPLATE: str = (
        "%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s"
    )
    TIMEZONE: str = "UTC"

    # Spimex parse settings
    BASE_URL: str = "https://spimex.com"
    TRADE_RESULTS_URL: str = "https://spimex.com/markets/oil_products/trades/results"
    DOWNLOAD_DIR: str = "downloads"
    AIOHTTP_TIMEOUT_TOTAL: int = 15
    START_PAGE: int = 1
    END_PAGE: int = 5
    
    
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, case_sensitive=True, extra="ignore"
    )


settings = Settings()
