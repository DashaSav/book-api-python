from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.models.converters.book_converter import BookConverter
from src.models.book import BookIn, BookOut

class BookRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: BookConverter):
        self.collection = collection
        self.converter = converter  # to_document() from_dcoument()


    async def get_by_id(self, id: str) -> BookOut | None:
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def create(self, book: BookIn) -> BookOut | None:
        inserted = await self.collection.insert_one(dict(book))
        
        document = await self.collection.find_one({"_id": inserted.inserted_id})
        return self.converter.from_document(document) if document else None

    async def update(self, id: str, updated_book: BookIn) -> BookOut | None:
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": updated_book})
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: str):
        await self.collection.delete_one({"_id": ObjectId(id)})
