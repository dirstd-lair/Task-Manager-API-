from fastapi import APIRouter, HTTPException, Depends, status
from app.utils.schemas.auth import (
    LoginModel, RegisterModel, RefreshModel, AuthResponseModel, 
    SuccessModel
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.utils.token import generate_auth_tokens, decode_access_token
from app.utils.password import hash_password, verify_password
from app.utils.auth import get_current_user
from app.database.models import User
from app.database import db 

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=AuthResponseModel)
async def register_router(data: RegisterModel):
    try:
        user_data = data.model_dump()
        user_data["password"] = hash_password(data.password)
        user = await db.user.create_new_user(user_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такой email уже занят"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обработке запроса"
        )
    
    tokens = generate_auth_tokens(user.id)
    return tokens

@router.post("/login", response_model=AuthResponseModel)
async def login_router(data: LoginModel):
    user = await db.user.get_user_by_email(data.email)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный email или password"
        )
    
    tokens = generate_auth_tokens(user.id)
    return tokens

@router.post("/refresh", response_model=AuthResponseModel)
async def refresh_router(data: RefreshModel):
    try:
        payload = decode_access_token(data.refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный токен"
        )
    
    if payload.get("type") != "refresh" or payload.get("sub") is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный тип токена"
        )
    
    user = await db.user.get_user_by_id(int(payload.get("sub")))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователя с таким токеном больше не существует"
        )
    
    tokens = generate_auth_tokens(user.id)
    return tokens
    
@router.delete("/deleted", response_model=SuccessModel)
async def delete_account_router(user: User = Depends(get_current_user)):
    try:
        is_deleted = await db.user.delete(user.id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить аккаунт"
        )
    
    if not is_deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить аккаунт"
        )
    
