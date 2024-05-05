from pydantic import BaseModel, EmailStr, Field

from src.models.common import PyObjectId


class BaseUser(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)


class UserIn(BaseUser):
    password: str = Field(min_length=8, max_length=30)


class UserUpdate(BaseUser):
    password: str | None = Field(min_length=8, max_length=30, default=None)


class UserUpsert(BaseUser):
    hash_password: str


class UserOut(BaseUser):
    id: PyObjectId = Field(alias="_id")


class UserInDB(UserOut):
    hash_password: str
