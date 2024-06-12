from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams
from src.models.common import PyObjectId
from src.models.converters.favorites_converter import FavoriteAuthorConverter
from src.models.favorite_author import FavoriteAuthorOut, FavoriteAuthorIn


class FavoriteAuthorsRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: FavoriteAuthorConverter):
        self.collection = collection
        self.converter = converter


    async def get_by_id(self, id: PyObjectId) -> FavoriteAuthorOut | None:
        document = await self.collection.aggregate([
            {"$match": {"_id": ObjectId(id)}},
        ]).next()

        return self.converter.from_document(document) if document else None
    

    async def get_by_user(self, user_id: PyObjectId, params: PagingParams) -> list[FavoriteAuthorOut]:
        docs = await self.collection.aggregate([
            {"$match": {"user_id": ObjectId(user_id)}},
            {"$skip": params.skip},
            {"$limit": params.limit}
        ]).to_list(params.limit)

        return [self.converter.from_document(author) for author in docs]
    

    async def create(self, author: FavoriteAuthorIn) -> FavoriteAuthorOut | None:
        inserted = await self.collection.insert_one(self.converter.to_document(author))
        
        document = await self.collection.aggregate([
            {"$match": {"_id": inserted.inserted_id}},
        ]).next()

        return self.converter.from_document(document) if document else None
    

    async def update(self, id: PyObjectId, updated_author: FavoriteAuthorIn) -> FavoriteAuthorOut | None:
        await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": self.converter.to_document(updated_author)}
        )

        document = await self.collection.aggregate([
            {"$match": {"_id": ObjectId(id)}},
        ]).next()

        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: PyObjectId):
        return await self.collection.delete_one({"_id": ObjectId(id)})
