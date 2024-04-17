from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)


class UserIn(BaseUser):
    password: str = Field(min_length=8, max_length=30)


class UserOut(BaseUser):
    id: str = Field(alias="_id")
