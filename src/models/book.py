from pydantic import BaseModel, Field

from src.models.user import BaseUser

from .common import PyObjectId


class BookIn(BaseModel):
    user_id: PyObjectId
    title: str
    description: str | None = None


class BookOut(BookIn):
    id: PyObjectId = Field(alias="_id")
    user: BaseUser
