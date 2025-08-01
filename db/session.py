from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config.settings import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(async_engine)
