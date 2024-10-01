from typing import AsyncGenerator, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings import settings
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


url = settings.DATABASE_URL_asyncpg
async_engine = create_async_engine(url)
new_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session

db_dependency = Annotated[AsyncSession, Depends(get_async_session)]