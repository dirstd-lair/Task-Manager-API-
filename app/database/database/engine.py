from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from ..models import Base 
from config import settings

from .methods import (
    UserMethods, TaskMethods
)

class Database:
    def __init__(self):
        self.engine = create_async_engine(settings.DATABASE_URL)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=True)
        self.user = UserMethods(self)
        self.task = TaskMethods(self)

    async def create_all_tables(self) -> None:
        async with self.engine.begin() as session:
            await session.run_sync(Base.metadata.create_all)