from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams
from src.models.converters.chapter_converter import ChapterConverter
from src.models.chapter import ChapterIn, ChapterOut

class ChapterRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: ChapterConverter):
        self.collection = collection
        self.converter = converter
    

    async def get_by_book(self, book_id: str, params: PagingParams) -> list[ChapterOut]:
        docs = await self.collection.find({"book_id": book_id}) \
                                .skip(params.skip) \
                                .limit(params.limit) \
                                .to_list(params.limit)

        return [self.converter.from_document(book) for book in docs]
    

    async def get_by_id(self, id: str) -> ChapterOut | None:
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def create(self, chapter: ChapterIn) -> ChapterOut | None:
        inserted = await self.collection.insert_one(dict(chapter))
        document = await self.collection.find_one({"_id": inserted.inserted_id})
        return self.converter.from_document(document) if document else None


    async def update(self, id: str, updated_chapter: ChapterIn) -> ChapterOut | None:
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": updated_chapter})
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: str):
        await self.collection.delete_one({"_id": ObjectId(id)})
