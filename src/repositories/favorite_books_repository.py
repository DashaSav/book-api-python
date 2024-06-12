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
        ]).next()

        return self.converter.from_document(document) if document else None
    

    async def get_by_user(self, user_id: PyObjectId, params: PagingParams) -> list[FavoriteBookOut]:
        docs = await self.collection.aggregate([
            {"$match": {"user_id": ObjectId(user_id)}},
            {"$skip": params.skip},
            {"$limit": params.limit}
        ]).to_list(params.limit)

        return [self.converter.from_document(book) for book in docs]
    

    async def create(self, book: FavoriteBookIn) -> FavoriteBookOut | None:
        inserted = await self.collection.insert_one(self.converter.to_document(book))
        
        document = await self.collection.aggregate([
            {"$match": {"_id": inserted.inserted_id}},
        ]).next()

        return self.converter.from_document(document) if document else None
    

    async def delete(self, user_id: PyObjectId, book_id: PyObjectId):
        return await self.collection.delete_one({
            "book_id": ObjectId(book_id),
            "user_id": ObjectId(user_id)
        })
