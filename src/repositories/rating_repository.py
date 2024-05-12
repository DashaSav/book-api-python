from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.models.common import PyObjectId
from src.models.converters.rating_converter import RatingConverter
from src.models.rating import RatingIn, RatingOut


class RatingRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: RatingConverter):
        self.collection = collection
        self.converter = converter


    async def get_by_id(self, id: PyObjectId) -> RatingOut | None:
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def get_by_book(self, book_id: PyObjectId) -> list[RatingOut]:
        docs = await self.collection.find({"book_id": ObjectId(book_id)}).to_list(None)
        return [self.converter.from_document(document) for document in docs]
    

    async def get_by_user(self, user_id: PyObjectId) -> list[RatingOut]:
        docs = await self.collection.find({"user_id": ObjectId(user_id)}).to_list(None)
        return [self.converter.from_document(document) for document in docs]
    

    async def get_by_user_and_book(self, user_id: PyObjectId, book_id: PyObjectId) -> RatingOut | None:
        document = await self.collection.find_one({
            "book_id": ObjectId(book_id),
            "user_id": ObjectId(user_id)
        })
        return self.converter.from_document(document) if document else None
    

    async def upsert(self, rating: RatingIn) -> RatingOut | None:
        upserted = await self.collection.update_one(
            {"book_id": ObjectId(rating.book_id), "user_id": ObjectId(rating.user_id)},
            {"$set": self.converter.to_document(rating)},
            upsert=True,
        )

        document = await self.collection.find_one({"_id": ObjectId(upserted.upserted_id)})

        if document:
            return self.converter.from_document(document)
        else:
            return await self.get_by_user_and_book(rating.user_id, rating.book_id)
    

    async def delete(self, id: PyObjectId):
        return await self.collection.delete_one({"_id": ObjectId(id)})
