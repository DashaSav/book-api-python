from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.models.user import BaseUser

from .common import PyObjectId


class BookIn(BaseModel):
    user_id: PyObjectId
    title: str
    tags: str | None = None
    summary: str | None = None
    comment_restriction: str | None = None
    age_restriction: str | None = None
    agreement: bool = True
    created_at: datetime = datetime.now()
    
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )


class BookOut(BookIn):
    id: PyObjectId = Field(alias="_id")


class BookWithUser(BookOut):    
    user: BaseUser
