from pydantic import BaseModel, Field

from src.models.user import UserOut

from .common import PyObjectId


class CommentIn(BaseModel):
    like: int
    author: UserOut
    content: str


class CommentOut(CommentIn):
    id: PyObjectId = Field(alias="_id")
