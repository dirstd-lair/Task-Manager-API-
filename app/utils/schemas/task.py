from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class NewTaskModel(BaseModel):
    title: Optional[str] = None 
    description: Optional[str] = None 

    @field_validator("description")
    def validate_title_description(cls, v, info):
        title = info.data.get("title")
        if not title and not v:
            raise ValueError("Хотя бы одно из полей (title или description) должно быть заполнено")
        
        if not title and v == "":
            raise ValueError("Если title не указан, description не может быть пустым")
            
        return v
    
    @field_validator("title")
    def validate_description_title(cls, v, info):
        description = info.data.get("description")
        if not v and not description:
            raise ValueError("Хотя бы одно из полей (title или description) должно быть заполнено")
            
        if not v and description == "":
            raise ValueError("Если description не указан, title не может быть пустым")
            
        return v
    
class EditTaskModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class SearchTaskModel(BaseModel):
    title: Optional[str] = None 
    description: Optional[str] = None
    
class TaskModel(BaseModel):
    id: int 
    title: Optional[str] = None 
    to_fix: bool
    description: str 
    created_at: datetime

class SuccessModel(BaseModel):
    ok: bool