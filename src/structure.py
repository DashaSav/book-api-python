from src.db import get_db, get_user_collection
from src.interactors.user_interactor import UserInteractor
from src.repositories.user_repository import UserRepository

db = get_db()

user_repository = UserRepository(get_user_collection(db))
user_interactor = UserInteractor(user_repository)
