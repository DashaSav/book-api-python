from pydantic import BaseModel, Field

from src.models.user import BaseUser

from .common import PyObjectId


class CommentIn(BaseModel):
    user_id: PyObjectId
    book_id: PyObjectId
    like: int = 0
    content: str


class CommentOut(CommentIn):
    id: PyObjectId = Field(alias="_id")
    user: BaseUser
