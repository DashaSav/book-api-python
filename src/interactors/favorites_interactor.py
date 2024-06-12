from src.api.general import PagingParams
from src.models.book import BookWithUser
from src.models.common import PyObjectId
from src.repositories.book_repository import BookRepository
from src.repositories.favorite_books_repository import FavoriteBooksRepository


class FavoritesInteractor:
    def __init__(
        self,
        book_repository: BookRepository,
        favorite_books_repository: FavoriteBooksRepository,
    ) -> None:
        self.book_repository = book_repository
        self.favorite_books_repository = favorite_books_repository


    async def get_user_favorite_books(
        self,
        user_id: PyObjectId,
        params: PagingParams
    ) -> list[BookWithUser]:
        favs = await self.favorite_books_repository.get_by_user(user_id, params)
        books = []

        for f in favs:
            book = await self.book_repository.get_by_id(f.book_id)
            books.append(book)

        return books    


