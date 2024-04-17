from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from passlib.context import CryptContext

from src.auth.jwt_bearer import JWTBearer, signJWT
from src.models.auth import AuthRequest, AuthResponse
from src.models.user import UserIn, UserInDB, UserOut
from src.db import get_user_collection
from src.serializers.user import to_user_out


router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", status_code=201)
async def create_user(
    user: UserIn,
    user_col: AsyncIOMotorCollection = Depends(get_user_collection)
) -> AuthResponse:
    db_user = await user_col.find_one({ "email": user.email })
    if db_user is not None:
       raise HTTPException(detail="User with this email already exists", status_code=404)

    hash_pass = pwd_context.hash(user.password)
    
    user_to_insert = {
        "name": user.name,
        "email": user.email,
        "hash_pass": hash_pass
    }

    inserted = await user_col.insert_one(user_to_insert)

    user_out = UserOut(_id=str(inserted.inserted_id), name=user.name, email=user.email)
    token = signJWT(user_out.id)

    return AuthResponse(user=user_out, token=token)


@router.post("/login")
async def login_user(
    user: AuthRequest,
    user_col: AsyncIOMotorCollection = Depends(get_user_collection)
) -> AuthResponse:
    db_user = await user_col.find_one({ "email": user.email })
    if not db_user:
       raise HTTPException(detail="User doesn't exist", status_code=404)
    
    if not pwd_context.verify(user.password, db_user["hash_pass"]):
        raise HTTPException(detail="Incorrect password", status_code=404)
    
    token = signJWT(str(db_user["_id"]))
    return AuthResponse(user=to_user_out(db_user), token=token)


@router.get("/{id}")
async def get_user(
    id: str, 
    user_col: AsyncIOMotorCollection = Depends(get_user_collection),
) -> UserOut:
    user = await user_col.find_one({"_id": ObjectId(id)})
    if user is None:
        raise HTTPException(detail="User not found", status_code=404)
    
    return to_user_out(user)


@router.get("/findByEmail/{email}")
async def get_user_by_email(
    email: str, 
    user_col: AsyncIOMotorCollection = Depends(get_user_collection)
) -> UserOut:
    user = await user_col.find_one({"email": email})
    if not user:
        raise HTTPException(detail="User not found", status_code=404)
    
    return to_user_out(user)


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_user(
    id: str,
    user: UserIn,
    user_col: AsyncIOMotorCollection = Depends(get_user_collection),
) -> UserOut:
    hash_pass = pwd_context.hash(user.password)
    updated_user = {
        "name": user.name,
        "email": user.email,
        "hash_pass": hash_pass
    }

    db_user = await user_col.find_one_and_update({"_id": ObjectId(id)}, {"$set": updated_user})

    if not db_user:
        raise HTTPException(detail="User not found", status_code=404)
    
    return to_user_out(await user_col.find_one({"_id": ObjectId(id)}))


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_user(
    id: str,
    user_col: AsyncIOMotorCollection = Depends(get_user_collection)
):
    await user_col.delete_one({"_id": ObjectId(id)})
