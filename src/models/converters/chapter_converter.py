from src.models.chapter import ChapterIn, ChapterOut


class ChapterConverter:
    def to_document(self, model: ChapterOut | ChapterIn):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return ChapterOut(**document)
