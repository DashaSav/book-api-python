from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams
from src.models.common import PyObjectId
from src.models.converters.report_converter import ReportConverter
from src.models.report import ReportIn, ReportOut


class ReportRepository:
    def __init__(self, collection: AsyncIOMotorCollection, converter: ReportConverter):
        self.collection = collection
        self.converter = converter


    async def get_by_id(self, id: PyObjectId) -> ReportOut | None:
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def get_all(self, params: PagingParams) -> list[ReportOut]:
        docs = await self.collection.find() \
            .skip(params.skip) \
            .limit(params.limit) \
            .to_list(params.limit)
        
        return [self.converter.from_document(document) for document in docs]
    

    async def create(self, report: ReportIn) -> ReportOut | None:
        inserted = await self.collection.insert_one(self.converter.to_document(report))
        document = await self.collection.find_one({"_id": inserted.inserted_id})
        return self.converter.from_document(document) if document else None


    async def update(self, id: PyObjectId, updated_report: ReportIn) -> ReportOut | None:
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": updated_report.model_dump()})
        document = await self.collection.find_one({"_id": ObjectId(id)})
        return self.converter.from_document(document) if document else None
    

    async def delete(self, id: PyObjectId):
        return await self.collection.delete_one({"_id": ObjectId(id)})
