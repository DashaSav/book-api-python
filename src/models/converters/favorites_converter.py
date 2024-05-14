from src.models.favorite_author import FavoriteAuthorOut
from src.models.favorite_book import FavoriteBookOut


class FavoriteAuthorConverter:
    def to_document(self, model):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return FavoriteAuthorOut(**document)


class FavoriteBookConverter:
    def to_document(self, model):
        return model.model_dump()

    
    def from_document(self, document: dict):
        return FavoriteBookOut(**document)
