from typing import Annotated
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.db import get_comment_collection
from src.models.comment import CommentOut, CommentIn


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_comment(
    comment: CommentIn,
    comment_col: AsyncIOMotorCollection = Depends(get_comment_collection)
) -> CommentOut | None:
    inserted = await comment_col.insert_one(dict(comment))
    return await comment_col.find_one(inserted.inserted_id)


@router.get("/")
async def get_comments(
    params: Annotated[PagingParams, Depends(paging_params)],
    comment_col: AsyncIOMotorCollection = Depends(get_comment_collection)
) -> list[CommentOut]:
    cursor = comment_col.find().skip(params.skip).limit(params.limit)
    return await cursor.to_list(params.limit)


@router.get("/{id}")
async def get_comment(id: str, comment_col: AsyncIOMotorCollection = Depends(get_comment_collection)) -> CommentOut:
    comment = await comment_col.find_one({"_id": ObjectId(id)})

    if comment is None:
        raise HTTPException(detail="Comment not found", status_code=404)
    
    return comment


@router.get("/findByAuthor/{author_id}")
async def get_book_by_author(
    author_id: str,
    params: Annotated[PagingParams, Depends(paging_params)],
    comment_col: AsyncIOMotorCollection = Depends(get_comment_collection)
) -> list[CommentOut]:
    cursor = comment_col.find({"author_id": author_id}).skip(params.skip).limit(params.limit)
    return await cursor.to_list(params.limit)


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_comment(
    id: str,
    comment: CommentIn,
    comment_col: AsyncIOMotorCollection = Depends(get_comment_collection)
) -> CommentOut:
    db_comment = await comment_col.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(comment)})

    if db_comment is None:
        raise HTTPException(detail="Comment not found", status_code=404)
    
    return db_comment


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_comment(
    id: str,
    comment_col: AsyncIOMotorCollection = Depends(get_comment_collection)
):
    await comment_col.delete_one({"_id": ObjectId(id)})
