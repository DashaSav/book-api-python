from typing import Annotated
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.db import get_chapter_collection
from src.models.chapter import ChapterOut, ChapterIn
from src.models.chapter import ChapterIn


router = APIRouter(prefix="/chapters", tags=["chapters"])


@router.post("/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_chapter(
    chapter: ChapterIn,
    chapter_col: AsyncIOMotorCollection = Depends(get_chapter_collection)
) -> ChapterOut | None:
    inserted = await chapter_col.insert_one(dict(chapter))

    inserted_chapter = await chapter_col.aggregate([
        {"$match": { "_id": inserted.inserted_id }},
        {"$lookup": { "from": "users", "localField": "user_id", "foreignField": "_id", "as": "user" }},
        {"$unwind": { "path": "$user" }}
    ]).to_list(length=1)

    return inserted_chapter[0]

@router.get("/")
async def get_chapters(
    params: Annotated[PagingParams, Depends(paging_params)],
    chapter_col: AsyncIOMotorCollection = Depends(get_chapter_collection)
) -> list[ChapterOut] | None:
    cursor = chapter_col.aggregate([
        {"$lookup": { "from": "users", "localField": "user_id", "foreignField": "_id", "as": "user" }},
        {"$unwind": { "path": "$user" }},
        {"$skip": params.skip},
        {"$limit": params.limit}
    ])

    return await cursor.to_list(params.limit)


@router.get("/{id}")
async def get_chapter(id: str, chapter_col: AsyncIOMotorCollection = Depends(get_chapter_collection)) -> ChapterOut:
    chapter = await chapter_col.find_one({"_id": ObjectId(id)})

    if chapter is None:
        raise HTTPException(detail="Chapter not found", status_code=404)
    
    return chapter


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_chapter(
    id: str,
    chapter: ChapterIn,
    chapter_col: AsyncIOMotorCollection = Depends(get_chapter_collection)
) -> ChapterOut:
    db_chapter = await chapter_col.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(chapter)})

    if db_chapter is None:
        raise HTTPException(detail="Chapter not found", status_code=404)
    
    return db_chapter


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_book(
    id: str,
    book_col: AsyncIOMotorCollection = Depends(get_chapter_collection)
):
    await book_col.delete_one({"_id": ObjectId(id)})
