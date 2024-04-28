from src.models.book import BookOut


class BookConverter:
    def to_document(self, model: BookOut):
        return model.model_dump(by_alias=True)

    
    def from_document(self, document: dict):
        return BookOut(**document)

