from src.models.book import BookIn, BookOut, BookWithUser


class BookConverter:
    def to_document(self, model: BookOut | BookIn | BookWithUser):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return BookWithUser(**document)

