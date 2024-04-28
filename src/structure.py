from src.db import get_db, get_user_collection
from src.interactors.user_interactor import UserInteractor
from src.models.converters.user_converter import UserConverter
from src.repositories.user_repository import UserRepository

from src.models.converters.book_converter import BookConverter
from src.repositories.book_repository import BookRepository

db = get_db()

user_converter = UserConverter()
user_repository = UserRepository(get_user_collection(db), user_converter)
user_interactor = UserInteractor(user_repository)

book_converter = BookConverter()
book_repository = Book_Repository(get_book_collection(db), book_converter)
