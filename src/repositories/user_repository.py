from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.models.converters.user_converter import UserConverter
from src.models.user import UserCreate, UserInDB, UserUpdate

class UserRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: UserConverter):
        self.collection = collection
        self.converter = converter  


    async def get_by_id(self, id: str) -> UserInDB | None:
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def get_by_email(self, email: str) -> UserInDB | None:
        document = await self.collection.find_one({"email": email})
        return self.converter.from_document(document) if document else None
    

    async def create(self, user: UserCreate) -> UserInDB | None:
        inserted = await self.collection.insert_one(dict(user))
        document = await self.collection.find_one({"_id": inserted.inserted_id})
        return self.converter.from_document(document) if document else None


    async def update(self, id: str, updated_user: UserUpdate) -> UserInDB | None:
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": updated_user})
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: str):
        await self.collection.delete_one({"_id": ObjectId(id)})
