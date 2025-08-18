from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.settings import DB_URL_asyncpg

async_engine = create_async_engine(
    url=DB_URL_asyncpg,
    echo=False,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(async_engine)
