from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.models.common import PyObjectId
from src.models.user import BaseUser


class FavoriteAuthorIn(BaseModel):
    user_id: PyObjectId
    author_id: PyObjectId

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class FavoriteAuthorOut(FavoriteAuthorIn):
    id: PyObjectId = Field(alias="_id")
