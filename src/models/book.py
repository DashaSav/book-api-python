from pydantic import BaseModel, Field

from .common import PyObjectId


class BookIn(BaseModel):
    title: str
    author: str
    description: str | None = None


class BookOut(BookIn):
    id: PyObjectId = Field(alias="_id")
