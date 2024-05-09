from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.models.user import BaseUser

from .common import PyObjectId


class CommentIn(BaseModel):
    user_id: PyObjectId
    book_id: PyObjectId
    like: int = 0
    content: str

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class CommentOut(CommentIn):
    id: PyObjectId = Field(alias="_id")
    user: BaseUser
