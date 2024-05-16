from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.models.common import PyObjectId


class BaseReport(BaseModel):
    user_id: PyObjectId
    report: str


class UserReportIn(BaseReport):
    reported_user_id: PyObjectId

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class UserReportOut(UserReportIn):
    id: PyObjectId = Field(alias="_id")


class BookReportIn(BaseReport):
    reported_book_id: PyObjectId

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class BookReportOut(BookReportIn):
    id: PyObjectId = Field(alias="_id")
