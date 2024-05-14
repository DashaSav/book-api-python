from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams
from src.models.common import PyObjectId
from src.models.converters.favorites_converter import FavoriteBookConverter
from src.models.favorite_book import FavoriteBookOut, FavoriteBookIn


class FavoriteBooksRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: FavoriteBookConverter):
        self.collection = collection
        self.converter = converter


    async def get_by_id(self, id: PyObjectId) -> FavoriteBookOut | None:
        document = await self.collection.aggregate([
            {"$match": {"_id": ObjectId(id)}},
            {"$lookup": { "from": "books", "localField": "book_id", "foreignField": "_id", "as": "book" }},
            {"$unwind": { "path": "$book" }},
            {"$lookup": { "from": "users", "localField": "user_id", "foreignField": "_id", "as": "user" }},
            {"$unwind": { "path": "$user" }},
        ]).next()

        return self.converter.from_document(document) if document else None
    

    async def get_by_user(self, user_id: PyObjectId, params: PagingParams) -> list[BookWithUser]:
        docs = await self.collection.aggregate([
            {"$match": {"user_id": ObjectId(user_id)}},
            {"$lookup": { "from": "users", "localField": "user_id", "foreignField": "_id", "as": "user" }},
            {"$unwind": { "path": "$user" }},
            {"$skip": params.skip},
            {"$limit": params.limit}
        ]).to_list(params.limit)

        return [self.converter.from_document(book) for book in docs]
    

    async def get_by_title(self, title: str, params: PagingParams) -> list[BookWithUser]:
        docs = await self.collection.aggregate([
            {"$match": {"title": {"$regex": title}}},
            {"$lookup": { "from": "users", "localField": "user_id", "foreignField": "_id", "as": "user" }},
            {"$unwind": { "path": "$user" }},
            {"$skip": params.skip},
            {"$limit": params.limit}
        ]).to_list(params.limit)

        return [self.converter.from_document(book) for book in docs]
    

    async def get_by_author(self, author: str, params: PagingParams) -> list[BookWithUser]:
        docs = await self.collection.aggregate([
            {"$lookup": { "from": "users", "localField": "user_id", "foreignField": "_id", "as": "user" }},
            {"$unwind": { "path": "$user" }},
            {"$match": {"user.name": {"$regex": author}}},
            {"$skip": params.skip},
            {"$limit": params.limit}
        ]).to_list(params.limit)
        
        return [self.converter.from_document(book) for book in docs]
    

    async def create(self, book: BookIn) -> BookWithUser | None:
        inserted = await self.collection.insert_one(self.converter.to_document(book))
        
        document = await self.collection.aggregate([
            {"$match": {"_id": inserted.inserted_id}},
            {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user"}},
            {"$unwind": {"path": "$user"}}
        ]).next()

        return self.converter.from_document(document) if document else None
    

    async def update(self, id: PyObjectId, updated_book: BookIn) -> BookWithUser | None:
        await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": self.converter.to_document(updated_book)}
        )

        document = await self.collection.aggregate([
            {"$match": {"_id": ObjectId(id)}},
            {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "_id", "as": "user"}},
            {"$unwind": {"path": "$user"}}
        ]).next()

        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: PyObjectId):
        return await self.collection.delete_one({"_id": ObjectId(id)})
