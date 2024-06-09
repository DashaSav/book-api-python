from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from src.models.common import PyObjectId


class BookRating(BaseModel):
    book_id: PyObjectId
    rating: int
    
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )
