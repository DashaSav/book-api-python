from src.models.rating import RatingIn, RatingOut


class RatingConverter:
    def to_document(self, model: RatingIn | RatingOut):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return RatingOut(**document)

