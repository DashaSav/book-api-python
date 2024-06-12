from src.db import (
    get_collection,
    get_db,
)

from src.models.converters.favorites_converter import FavoriteAuthorConverter, FavoriteBookConverter
from src.models.converters.rating_converter import RatingConverter
from src.models.converters.user_converter import UserConverter
from src.models.converters.book_converter import BookConverter
from src.models.converters.comment_converter import CommentConverter
from src.models.converters.chapter_converter import ChapterConverter
from src.models.converters.report_converter import BookReportConverter, BookReportConverter, UserReportConverter

from src.repositories.book_report_repository import BookReportRepository
from src.repositories.favorite_authors_repository import FavoriteAuthorsRepository
from src.repositories.favorite_books_repository import FavoriteBooksRepository
from src.repositories.rating_repository import RatingRepository
from src.repositories.user_repository import UserRepository
from src.repositories.book_repository import BookRepository
from src.repositories.comment_repository import CommentRepository
from src.repositories.chapter_repository import ChapterRepository
from src.repositories.user_report_repository import UserReportRepository

from src.interactors.user_interactor import UserInteractor
from src.interactors.book_interactor import BookInteractor
from src.interactors.favorites_interactor import FavoritesInteractor


db = get_db()

user_converter = UserConverter()
book_converter = BookConverter()
comment_converter = CommentConverter()
chapter_converter = ChapterConverter()
user_report_converter = UserReportConverter()
book_report_converter = BookReportConverter()
favorite_book_converter = FavoriteBookConverter()
favorite_author_converter = FavoriteAuthorConverter()
rating_converter = RatingConverter()

user_repository = UserRepository(get_collection(db, "users"), user_converter)
book_repository = BookRepository(get_collection(db, "books"), book_converter)
comment_repository = CommentRepository(get_collection(db, "comments"), comment_converter)
chapter_repository = ChapterRepository(get_collection(db, "chapters"), chapter_converter)
user_report_repository = UserReportRepository(get_collection(db, "user_reports"), user_report_converter)
book_report_repository = BookReportRepository(get_collection(db, "book_reports"), book_report_converter)
favorite_books_repository = FavoriteBooksRepository(
    get_collection(db, "favorite_books"), 
    favorite_book_converter
)
favorite_authors_repository = FavoriteAuthorsRepository(
    get_collection(db, "favorite_authors"), 
    favorite_author_converter
)
rating_repository = RatingRepository(get_collection(db, "ratings"), rating_converter)

user_interactor = UserInteractor(user_repository)
book_interactor = BookInteractor(book_repository, rating_repository)
favorites_interactor = FavoritesInteractor(book_repository, favorite_books_repository)
