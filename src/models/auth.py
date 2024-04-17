from pydantic import BaseModel, EmailStr
from user import UserOut as User

class AuthRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(AuthRequest):
    name: str


class AuthResponse(BaseModel):
    user: User | None = None
    token: str | None = None
