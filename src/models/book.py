from pydantic import BaseModel, Field


class BookIn(BaseModel):
    title: str
    author: str
    description: str


class BookOut(BookIn):
    id: str = Field(alias="_id")
