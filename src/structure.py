from src.db import (
    get_collection,
    get_db,
)

from src.models.converters.rating_converter import RatingConverter
from src.models.converters.user_converter import UserConverter
from src.models.converters.book_converter import BookConverter
from src.models.converters.comment_converter import CommentConverter
from src.models.converters.chapter_converter import ChapterConverter
from src.models.converters.report_converter import ReportConverter

from src.repositories.rating_repository import RatingRepository
from src.repositories.user_repository import UserRepository
from src.repositories.book_repository import BookRepository
from src.repositories.comment_repository import CommentRepository
from src.repositories.chapter_repository import ChapterRepository
from src.repositories.report_repository import ReportRepository

from src.interactors.user_interactor import UserInteractor


db = get_db()

user_converter = UserConverter()
book_converter = BookConverter()
comment_converter = CommentConverter()
chapter_converter = ChapterConverter()
report_converter = ReportConverter()
rating_converter = RatingConverter()

user_repository = UserRepository(get_collection(db, "users"), user_converter)
book_repository = BookRepository(get_collection(db, "books"), book_converter)
comment_repository = CommentRepository(get_collection(db, "comments"), comment_converter)
chapter_repository = ChapterRepository(get_collection(db, "chapters"), chapter_converter)
report_repository = ReportRepository(get_collection(db, "reports"), report_converter)
rating_repository = RatingRepository(get_collection(db, "ratings"), rating_converter)

user_interactor = UserInteractor(user_repository)
