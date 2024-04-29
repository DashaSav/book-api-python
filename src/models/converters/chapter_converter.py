from src.models.chapter import ChapterOut


class ChapterConverter:
    def to_document(self, model: ChapterOut):
        return model.model_dump(by_alias=True)

    
    def from_document(self, document: dict):
        return ChapterOut(**document)
