from sqlalchemy import select, update, delete 
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.database.models import User 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..engine import Database

class UserMethods:
    def __init__(self, db: "Database"):
        self.db = db 

    async def create_new_user(self, data: dict) -> User | None:
        async with self.db.async_session() as session:
            try:
                new_user = User(**data)
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
                return new_user
            
            except IntegrityError:
                await session.rollback()
                raise 
            except Exception:
                await session.rollback()
                raise 
            
    async def get_user_by_email(self, email: str) -> User | None:
        async with self.db.async_session() as session:
            try:
                result = await session.execute(
                    select(User).where(User.email == email)
                )
                return result.scalar_one_or_none()
            except SQLAlchemyError:
                return None
            
    async def get_user_by_id(self, id: str) -> User | None:
        async with self.db.async_session() as session:
            try:
                result = await session.execute(
                    select(User).where(User.id == id)
                )
                return result.scalar_one_or_none()
            except SQLAlchemyError:
                return None

    async def delete(self, user_id: int) -> bool:
        async with self.db.async_session() as session:
            try:
                result = await session.execute(
                    delete(User).where(User.id == user_id)
                )
                session.add(result)
                await session.commit()
                return result.rowcount > 0
            except SQLAlchemyError as ex:
                print(ex)
                return None 
            except Exception as ex:
                print(ex)
                raise