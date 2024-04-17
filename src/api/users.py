from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
from passlib.context import CryptContext

from src.models.user import UserIn, UserOut
from src.db import get_user_collection
from src.serializers.user import to_user_out


router = APIRouter(prefix="/users", tags=["users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", status_code=201)
async def create_user(
    user: UserIn,
    user_col: AsyncIOMotorCollection = Depends(get_user_collection)
):
    db_user = await user_col.find_one({ "email": user.email })
    if db_user is not None:
       raise HTTPException(detail="User with this email already exists", status_code=404)

    hashed_password = pwd_context.hash(user.password)
    
    user_to_insert = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    }

    inserted = await user_col.insert_one(user_to_insert)

    return UserOut(_id=str(inserted.inserted_id), name=user.name, email=user.email)


@router.get("/{id}")
async def get_user(id: str, user_col: AsyncIOMotorCollection = Depends(get_user_collection)) -> UserOut:
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
    if user is None:
        raise HTTPException(detail="User not found", status_code=404)
    
    return to_user_out(user)


@router.put("/{id}")
async def update_user(
    id: str,
    user: UserIn,
    user_col: AsyncIOMotorCollection = Depends(get_user_collection)
) -> UserOut:
    db_user = await user_col.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})

    if db_user is None:
        raise HTTPException(detail="User not found", status_code=404)
    
    return to_user_out(db_user)
