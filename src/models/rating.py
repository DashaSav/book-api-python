from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.models.common import PyObjectId


class RatingIn(BaseModel):
    user_id: PyObjectId
    book_id: PyObjectId
    grade: int = Field(ge=1, le=5)

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class RatingOut(RatingIn):
    id: PyObjectId = Field(alias="_id")
