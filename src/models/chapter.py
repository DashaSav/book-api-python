from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.models.common import PyObjectId


class ChapterIn(BaseModel):
    book_id: PyObjectId
    title: str
    text: str | None = None
    comment: str | None = None

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class ChapterOut(ChapterIn):
    id: PyObjectId = Field(alias="_id")
