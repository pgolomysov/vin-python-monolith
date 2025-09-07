from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_async_engine(settings.database_url)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

sync_engine = create_engine(settings.alembic_database_url, echo=True, future=True)
sync_session = sessionmaker(bind=sync_engine, class_=Session, expire_on_commit=False)

def get_sync_session() -> Session:
    with sync_session() as session:
        yield session