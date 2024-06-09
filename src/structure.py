from src.db import (
    get_collection,
    get_db,
)

from src.models.converters.rating_converter import RatingConverter
from src.models.converters.user_converter import UserConverter
from src.models.converters.book_converter import BookConverter
from src.models.converters.comment_converter import CommentConverter
from src.models.converters.chapter_converter import ChapterConverter
from src.models.converters.report_converter import BookReportConverter, BookReportConverter, UserReportConverter

from src.repositories.book_report_repository import BookReportRepository
from src.repositories.rating_repository import RatingRepository
from src.repositories.user_repository import UserRepository
from src.repositories.book_repository import BookRepository
from src.repositories.comment_repository import CommentRepository
from src.repositories.chapter_repository import ChapterRepository
from src.repositories.user_report_repository import UserReportRepository

from src.interactors.user_interactor import UserInteractor
from src.interactors.book_interactor import BookInteractor


db = get_db()

user_converter = UserConverter()
book_converter = BookConverter()
comment_converter = CommentConverter()
chapter_converter = ChapterConverter()
user_report_converter = UserReportConverter()
book_report_converter = BookReportConverter()
rating_converter = RatingConverter()

user_repository = UserRepository(get_collection(db, "users"), user_converter)
book_repository = BookRepository(get_collection(db, "books"), book_converter)
comment_repository = CommentRepository(get_collection(db, "comments"), comment_converter)
chapter_repository = ChapterRepository(get_collection(db, "chapters"), chapter_converter)
user_report_repository = UserReportRepository(get_collection(db, "user_reports"), user_report_converter)
book_report_repository = BookReportRepository(get_collection(db, "book_reports"), book_report_converter)
rating_repository = RatingRepository(get_collection(db, "ratings"), rating_converter)

user_interactor = UserInteractor(user_repository)
book_interactor = BookInteractor(book_repository, rating_repository)
