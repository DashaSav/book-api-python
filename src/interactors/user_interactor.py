from src.auth.jwt_bearer import signJWT
from src.models.auth import AuthRequest
from src.models.common import PyObjectId
from src.models.token import Token
from src.models.user import UserUpsert, UserIn, UserOut, UserUpdate
from src.repositories.user_repository import UserRepository

from passlib.context import CryptContext


class UserInteractor:
    def __init__(
        self, 
        repository: UserRepository,
        pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ):
        self.repository = repository
        self.pwd_context = pwd_context
    

    async def create_user(self, user: UserIn) -> tuple[UserOut, Token] | None:
        if await self.repository.get_by_email(user.email):
            return None
        
        hash_password = self.pwd_context.hash(user.password)
    
        user_to_insert = {
            "name": user.name,
            "email": user.email,
            "hash_password": hash_password
        }
        created_user = await self.repository.create(UserUpsert(**user_to_insert))
        
        if not created_user:
            return None
        
        token = signJWT(created_user.id)
        return (created_user, token)
    

    async def login(self, request: AuthRequest) -> tuple[UserOut, Token] | None:
        db_user = await self.repository.get_by_email(request.email)
        if not db_user:
            return None
        
        if not self.pwd_context.verify(request.password, db_user.hash_password):
            return None
    
        token = signJWT(str(db_user.id))
        return (db_user, token)
    

    async def update_user(self, id: PyObjectId, user: UserUpdate) -> UserOut | None:
        db_user = await self.repository.get_by_id(id)
        if not db_user:
            return None
        
        if (user.password):
            hash_password = self.pwd_context.hash(user.password)

        updated_user = {
            "name": user.name,
            "email": user.email
        }

        if hash_password:
            updated_user["hash_password"] = hash_password
        else:
            updated_user["hash_password"] = db_user.hash_password

        return await self.repository.update(id, UserUpsert(**updated_user))
