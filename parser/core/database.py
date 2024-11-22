from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from parser.core.config import settings


engine = create_async_engine(
    settings.asyncpg_url.unicode_string(), echo=settings.ECHO_SQL
)

AsyncSessionFactory = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False
)
