from pydantic import BaseModel, EmailStr
from .token import Token
from .user import UserOut

class AuthRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    user: UserOut | None = None
    token: Token | None = None
