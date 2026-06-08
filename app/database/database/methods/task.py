from sqlalchemy import select, update, delete, or_
from sqlalchemy.exc import SQLAlchemyError
from app.database.models import Task 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..engine import Database

class TaskMethods:
    def __init__(self, db: "Database"):
        self.db = db 

    async def create_task(self, data: dict) -> Task | None:
        async with self.db.async_session() as session:
            try:
                new_task = Task(**data)
                session.add(new_task)
                await session.commit()
                await session.refresh(new_task)
                return new_task
            except SQLAlchemyError as ex:
                print(ex)
                await session.rollback()
                raise 
            except Exception:
                raise 
            
    async def get_task_by_id(self, task_id: int, user_id: int) -> Task | None:
        async with self.db.async_session() as session:
            try:
                result = await session.execute(
                    select(Task).where(Task.id == task_id)
                    .where(Task.user_id == user_id)
                )
                return result.scalar_one_or_none()
            except SQLAlchemyError:
                await session.rollback()
                raise 
            except Exception:
                raise 
            
    async def get_tasks(self, user_id: int) -> list[Task] | None:
        async with self.db.async_session() as session:
            try:
                result = await session.execute(
                    select(Task)
                    .where(Task.user_id == user_id)
                )
                return result.scalars().all()
            except SQLAlchemyError:
                await session.rollback()
                raise 
            except Exception:
                raise 

    async def search_tasks(self,
                       user_id: int,
                       title: str = None,
                       description: str = None) -> list[Task]:
        async with self.db.async_session() as session:
            query = select(Task).where(Task.user_id == user_id)
        
            search_filters = []
            if title:
                search_filters.append(Task.title.ilike(f"%{title}%"))
            if description:
                search_filters.append(Task.description.ilike(f"%{description}%"))
                
            if search_filters:
                query = query.where(or_(*search_filters))

            result = await session.execute(query)
            return result.scalars().all()

    async def edit_tasks(self, data: dict, task_id: int,
                         user_id: int) -> Task | None:
        async with self.db.async_session() as session:
            try:
                updated_dict = {k: v for k, v in data.items() if v is not None}
                if not updated_dict:
                    return await self.get_task_by_id(task_id, user_id)
                
                result = await session.execute(
                    update(Task).where(Task.id == task_id)
                    .values(**updated_dict)
                )
                await session.commit()
                return await self.get_task_by_id(task_id, user_id)
            
            except SQLAlchemyError as ex:
                await session.rollback()
                raise 
            except Exception as ex:
                raise 
            
    async def delete_task(self, task_id: int, user_id: int) -> bool:
        async with self.db.async_session() as session:
            try:
                result = await session.execute(
                    delete(Task).where(Task.id == task_id)
                    .where(Task.user_id == user_id)
                )
                await session.commit()
                return result.rowcount > 0
            except SQLAlchemyError as ex:
                await session.rollback()
                raise 
            except Exception as ex:
                raise 
            
    async def fixed_task(self, task_id: int, user_id: int, to_fix: bool) -> bool:
        async with self.db.async_session() as session:
            try:
                result = await session.execute(
                    update(Task).where(Task.id == task_id)
                    .where(Task.user_id == user_id)
                    .values(to_fix=to_fix)
                )
                await session.commit()
                return result.rowcount > 0
            except SQLAlchemyError as ex:
                await session.rollback()
                raise 
            except Exception as ex:
                raise 

