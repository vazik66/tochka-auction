import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    password_confirm: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDBBase(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str

    class Config:
        orm_mode = True


class UserFullName(BaseModel):
    full_name: str


# Public Scheme to return to user
class User(UserInDBBase):
    pass


# Actual database scheme
class UserInDB(UserInDBBase):
    password_hash: str
    is_superuser: bool = False
