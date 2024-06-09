from src.models.book_rating import BookRating
from src.models.common import PyObjectId
from src.repositories.book_repository import BookRepository
from src.repositories.rating_repository import RatingRepository


class BookInteractor:
    def __init__(
        self,
        book_repository: BookRepository, 
        rating_repository: RatingRepository
    ) -> None:
        self.book_repository = book_repository
        self.rating_repository = rating_repository


    async def get_rating(self, book_id: PyObjectId) -> BookRating | None:
        book_ratings = await self.rating_repository.get_by_book(book_id)

        try:
            s = 0
            for r in book_ratings: s += r.grade
            return BookRating(book_id=book_id, rating=(s // len(book_ratings)))
        except:
            return None
