from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

MIN_NAME_LENGTH = 4
MAX_NAME_LENGTH = 100


class UserBase(BaseModel):
    email: EmailStr  # unique value among all users
    name: str = Field(min_length=MIN_NAME_LENGTH, max_length=MAX_NAME_LENGTH)


class UserCreate(UserBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserRead(UserBase):
    created_at: datetime
    deleted_at: Optional[datetime]
