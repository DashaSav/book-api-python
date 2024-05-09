from src.models.book import BookIn, BookOut


class BookConverter:
    def to_document(self, model: BookOut | BookIn):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return BookOut(**document)

