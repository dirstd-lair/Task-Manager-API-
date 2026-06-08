from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func
from datetime import datetime
from .base import Base 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(55), unique=True)
    password: Mapped[str] = mapped_column(String(1024))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now())
    
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="user")
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at
        }