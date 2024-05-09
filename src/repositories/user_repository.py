from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.models.common import PyObjectId
from src.models.converters.user_converter import UserConverter
from src.models.user import UserUpsert, UserInDB

class UserRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: UserConverter):
        self.collection = collection
        self.converter = converter  


    async def get_by_id(self, id: PyObjectId) -> UserInDB | None:
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def get_by_email(self, email: str) -> UserInDB | None:
        document = await self.collection.find_one({"email": email})
        return self.converter.from_document(document) if document else None
    
    # object ? update : insert => upsert
    async def create(self, user: UserUpsert) -> UserInDB | None:
        inserted = await self.collection.insert_one(self.converter.to_document(user))
        document = await self.collection.find_one({"_id": inserted.inserted_id})
        return self.converter.from_document(document) if document else None


    async def update(self, id: PyObjectId, updated_user: UserUpsert) -> UserInDB | None:
        await self.collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": self.converter.to_document(updated_user)}
        )

        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: PyObjectId):
        await self.collection.delete_one({"_id": ObjectId(id)})
