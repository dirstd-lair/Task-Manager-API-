from datetime import datetime, timedelta, timezone
from jose import jwt, ExpiredSignatureError
from config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_TOKEN, algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_TOKEN, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError as ex:
        raise 
    except jwt.JWTError as ex:
        raise 

def generate_auth_tokens(user_id: int):
    access_token = create_access_token(
        data={
            "sub": str(user_id),
            "type": "bearer"
        }, 
        expires_delta=timedelta(days=1)
    )
    
    refresh_token = create_access_token(
        data={
            "sub": str(user_id),
            "type": "refresh"
        }, 
        expires_delta=timedelta(days=7)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
