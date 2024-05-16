from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams
from src.models.common import PyObjectId
from src.models.converters.report_converter import BookReportConverter
from src.models.report import BookReportIn, BookReportOut


class BookReportRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: BookReportConverter):
        self.collection = collection
        self.converter = converter


    async def get_by_id(self, id: PyObjectId) -> BookReportOut | None:
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def get_all(self, params: PagingParams) -> list[BookReportOut]:
        docs = await self.collection.find() \
            .skip(params.skip) \
            .limit(params.limit) \
            .to_list(params.limit)
        
        return [self.converter.from_document(document) for document in docs]
    

    async def create(self, report: BookReportIn) -> BookReportOut | None:
        inserted = await self.collection.insert_one(self.converter.to_document(report))
        document = await self.collection.find_one({"_id": inserted.inserted_id})
        return self.converter.from_document(document) if document else None


    async def update(self, id: PyObjectId, updated_report: BookReportIn) -> BookReportOut | None:
        await self.collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": self.converter.to_document(updated_report)}
        )
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: PyObjectId):
        return await self.collection.delete_one({"_id": ObjectId(id)})
