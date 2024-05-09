from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams
from src.models.common import PyObjectId
from src.models.converters.comment_converter import CommentConverter
from src.models.comment import CommentIn, CommentOut

class CommentRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: CommentConverter):
        self.collection = collection
        self.converter = converter
    

    async def get_by_book(self, book_id: PyObjectId, params: PagingParams) -> list[CommentOut]:
        docs = await self.collection.aggregate([
            {"$match": {"book_id": ObjectId(book_id)}},
            {"$lookup": { "from": "users", "localField": "user_id", "foreignField": "_id", "as": "user" }},
            {"$unwind": { "path": "$user" }},
            {"$skip": params.skip},
            {"$limit": params.limit}
        ]).to_list(params.limit)

        return [self.converter.from_document(book) for book in docs]
    

    async def get_by_user(self, user_id: PyObjectId, params: PagingParams) -> list[CommentOut]:
        docs = await self.collection.aggregate([
            {"$match": {"user_id": ObjectId(user_id)}},
            {"$lookup": { "from": "users", "localField": "user_id", "foreignField": "_id", "as": "user" }},
            {"$unwind": { "path": "$user" }},
            {"$skip": params.skip},
            {"$limit": params.limit}
        ]).to_list(params.limit)

        return [self.converter.from_document(book) for book in docs]


    async def get_by_id(self, id: PyObjectId) -> CommentOut | None:
        document = await self.collection.aggregate([
            {"$match": {"_id": ObjectId(id)}},
            {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user"}},
            {"$unwind": {"path": "$user"}}
        ]).next()

        return self.converter.from_document(document) if document else None
    

    async def create(self, comment: CommentIn) -> CommentOut | None:
        inserted = await self.collection.insert_one(self.converter.to_document(comment))
        
        document = await self.collection.aggregate([
            {"$match": {"_id": inserted.inserted_id}},
            {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user"}},
            {"$unwind": {"path": "$user"}}
        ]).next()

        return self.converter.from_document(document) if document else None


    async def update(self, id: PyObjectId, updated_comment: CommentIn) -> CommentOut | None:
        await self.collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": self.converter.to_document(updated_comment)}
        )

        document = await self.collection.aggregate([
            {"$match": {"_id": ObjectId(id)}},
            {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user"}},
            {"$unwind": {"path": "$user"}}
        ]).next()

        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: PyObjectId):
        await self.collection.delete_one({"_id": ObjectId(id)})
