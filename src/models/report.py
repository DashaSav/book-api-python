from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.models.common import PyObjectId


class ReportIn(BaseModel):
    user_id: PyObjectId
    reported_user_id: PyObjectId
    report: str

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel
    )


class ReportOut(ReportIn):
    id: PyObjectId = Field(alias="_id")
