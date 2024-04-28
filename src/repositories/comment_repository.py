from tokenize import Comment
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.models.converters.comment_converter import CommentConverter
from src.models.comment import CommentIn, CommentOut

class CommentRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: CommentConverter):
        self.collection = collection
        self.converter = converter  # to_document() from_dcoument()


    async def get_by_id(self, id: str) -> CommentOut | None:
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def create(self, comment: CommentIn) -> CommentOut | None:
        inserted = await self.collection.insert_one(dict(comment))
        
        document = await self.collection.find_one({"_id": inserted.inserted_id})
        return self.converter.from_document(document) if document else None

    async def update(self, id: str, updated_comment: CommentIn) -> CommentOut | None:
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": updated_comment})
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: str):
        await self.collection.delete_one({"_id": ObjectId(id)})
