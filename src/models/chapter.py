from pydantic import BaseModel, Field

from .common import PyObjectId


class ChapterIn(BaseModel):
    user_id: PyObjectId
    book_id: PyObjectId
    title: str
    text: str | None = None


class ChapterOut(ChapterIn):
    id: PyObjectId = Field(alias="_id")
