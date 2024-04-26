from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.models.user import UserCreate, UserInDB, UserUpdate

class UserRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection


    async def get_by_id(self, id: str) -> UserInDB | None:
       return await self.collection.find_one({"_id": ObjectId(id)})
    

    async def get_by_email(self, email: str) -> UserInDB | None:
       return await self.collection.find_one({"email": email})
    

    async def create(self, user: UserCreate) -> UserInDB | None:
        inserted = await self.collection.insert_one(dict(user))
        return await self.collection.find_one({"_id": inserted.inserted_id})
    

    async def update(self, id: str, updated_user: UserUpdate) -> UserInDB | None:
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": updated_user})
        return await self.collection.find_one({"_id": ObjectId(id)})
    

    async def delete(self, id: str):
        await self.collection.delete_one({"_id": ObjectId(id)})
