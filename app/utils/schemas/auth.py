from pydantic import BaseModel, EmailStr, Field

class LoginModel(BaseModel):
    email: EmailStr 
    password: str = Field(..., min_length=6, max_length=50)

class RegisterModel(BaseModel):
    email: EmailStr
    password: str 

class RefreshModel(BaseModel):
    refresh_token: str 

class AuthResponseModel(BaseModel):
    access_token: str 
    refresh_token:str 

class SuccessModel(BaseModel):
    ok: bool