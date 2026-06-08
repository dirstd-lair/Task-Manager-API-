from fastapi import APIRouter, HTTPException, Depends, status
from app.utils.schemas.task import (
    NewTaskModel, EditTaskModel, TaskModel,
    SearchTaskModel, SuccessModel
)
from app.utils.auth import get_current_user
from app.database import db 
from app.database.models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/create", response_model=TaskModel)
async def create_task_router(data: NewTaskModel,
                             user: User = Depends(get_current_user)):
    try:
        task_data = data.model_dump()
        task_data["user_id"] = user.id
        task = await db.task.create_task(task_data)
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обработке запроса"
        )
    return task

@router.get("/all", response_model=list[TaskModel])
async def get_all_tasks_router(user: User = Depends(get_current_user)):
    try:
        tasks = await db.task.get_tasks(user.id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обработке запроса"
        )
    return tasks

@router.patch("/{task_id}", response_model=TaskModel)
async def edit_task_router(task_id: int, data: EditTaskModel,
                           user: User = Depends(get_current_user)):
    try:
        task = await db.task.get_task_by_id(task_id, user.id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обработке запроса"
        )
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    
    try:
        task_data = data.model_dump(exclude={"task_id"}, exclude_unset=True)
        new_task = await db.task.edit_tasks(task_data, task_id, user.id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось обновить задачу"
        )
    
    return new_task

@router.delete("/{task_id}", response_model=SuccessModel)
async def delete_task_router(task_id: int, 
                             user: User = Depends(get_current_user)):
    task = await db.task.get_task_by_id(task_id, user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )

    try:
        is_deleted = await db.task.delete_task(task_id, user.id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить задачу"
        )
    
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить задачу"
        )
    
    return SuccessModel(
        ok=True
    )
    
@router.post("/fixed/{task_id}", response_model=SuccessModel)
async def fixed_task_router(task_id: int, to_fix: bool = False,
                             user: User = Depends(get_current_user)):
    try:
        is_fixed = await db.task.fixed_task(task_id, user.id, to_fix)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось закрепить задачу"
        )
    
    if not is_fixed:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось закрепить задачу"
        )
    
    return SuccessModel(
        ok=True
    )
    
@router.get("/search", response_model=list[TaskModel])
async def search_task_router(data: SearchTaskModel = Depends(),
                             user: User = Depends(get_current_user)):
    try:
        tasks = await db.task.search_tasks(user.id,
                                           title=data.title,
                                           description=data.description)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось провести поиск"
        )
    
    return tasks