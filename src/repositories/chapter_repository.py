from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams
from src.models.common import PyObjectId
from src.models.converters.chapter_converter import ChapterConverter
from src.models.chapter import ChapterIn, ChapterOut

class ChapterRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: ChapterConverter):
        self.collection = collection
        self.converter = converter


    async def get_by_id(self, id: PyObjectId) -> ChapterOut | None:
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def get_by_book(self, book_id: PyObjectId, params: PagingParams) -> list[ChapterOut]:
        docs = await self.collection.find({"book_id": ObjectId(book_id)}) \
            .skip(params.skip) \
            .limit(params.limit) \
            .to_list(params.limit)
        
        return [self.converter.from_document(document) for document in docs]
    

    async def create(self, chapter: ChapterIn) -> ChapterOut | None:
        inserted = await self.collection.insert_one(self.converter.to_document(chapter))
        document = await self.collection.find_one({"_id": inserted.inserted_id})
        return self.converter.from_document(document) if document else None


    async def update(self, id: PyObjectId, updated_chapter: ChapterIn) -> ChapterOut | None:
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": updated_chapter.model_dump()})
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: PyObjectId):
        return await self.collection.delete_one({"_id": ObjectId(id)})
