from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.config import settings

# from app.config import (
#     POSTGRES_DB_NAME,
#     POSTGRES_HOST,
#     POSTGRES_PASSWORD,
#     POSTGRES_PORT,
#     POSTGRES_USER
# )

# DATABASE_URL = (f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
#                 f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}')

engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
