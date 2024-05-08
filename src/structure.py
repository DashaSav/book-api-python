from src.db import (
    get_chapter_collection,
    get_db, 
    get_user_collection,
    get_book_collection,
    get_comment_collection
)

from src.models.converters.user_converter import UserConverter
from src.models.converters.book_converter import BookConverter
from src.models.converters.comment_converter import CommentConverter
from src.models.converters.chapter_converter import ChapterConverter

from src.repositories.user_repository import UserRepository
from src.repositories.book_repository import BookRepository
from src.repositories.comment_repository import CommentRepository
from src.repositories.chapter_repository import ChapterRepository

from src.interactors.user_interactor import UserInteractor


db = get_db()

user_converter = UserConverter()
book_converter = BookConverter()
comment_converter = CommentConverter()
chapter_converter = ChapterConverter()

user_repository = UserRepository(get_user_collection(db), user_converter)
book_repository = BookRepository(get_book_collection(db), book_converter)
comment_repository = CommentRepository(get_comment_collection(db), comment_converter)
chapter_repository = ChapterRepository(get_chapter_collection(db), chapter_converter)

user_interactor = UserInteractor(user_repository)
