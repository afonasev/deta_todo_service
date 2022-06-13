from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, Field

MIN_USER_NAME_LENGTH = 4
MAX_USER_NAME_LENGTH = 50


class UserBase(BaseModel):
    name: str = Field(min_length=MIN_USER_NAME_LENGTH, max_length=MAX_USER_NAME_LENGTH)
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: UUID4
    created_at: datetime
    deleted_at: datetime | None
