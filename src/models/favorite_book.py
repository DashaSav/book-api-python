from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.models.book import BookOut
from src.models.common import PyObjectId


class FavoriteBookIn(BaseModel):
    user_id: PyObjectId
    book_id: PyObjectId

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class FavoriteBookOut(FavoriteBookIn):
    id: PyObjectId = Field(alias="_id")
