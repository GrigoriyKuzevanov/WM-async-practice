from parser.core.config import settings
from typing import Any

from alembic.config import CommandLine, Config


def make_config() -> Config:
    """
    Создает и настривает объект конфигурации Alembic, используя настройки приложения.
    """

    alembic_config = Config()
    alembic_config.set_main_option("script_location", settings.SCRIPT_LOCATION)
    alembic_config.set_main_option("version_locations", settings.VERSION_LOCATIONS)
    alembic_config.set_main_option(
        "sqlalchemy.url", settings.asyncpg_url.unicode_string()
    )
    alembic_config.set_main_option("file_template", settings.FILE_TEMPLATE)
    alembic_config.set_main_option("timezone", settings.TIMEZONE)

    return alembic_config


def alembic_runner(*args: Any) -> None:
    """
    Запускает Alembic c переданными аргументами командной строки и текущей конфигурацией.

    Args:
        args (Any): Аргументы командной строки
    """

    cli = CommandLine()
    cli.run_cmd(make_config(), cli.parser.parse_args(args))
