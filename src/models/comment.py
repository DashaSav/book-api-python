from pydantic import BaseModel, Field

from .common import PyObjectId


class CommentIn(BaseModel):
    user_id: PyObjectId
    like: int = 0
    content: str


class CommentOut(CommentIn):
    id: PyObjectId = Field(alias="_id")
