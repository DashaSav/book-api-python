from typing import Annotated
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.db import get_book_collection
from src.models.book import BookOut, BookIn


router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_book(
    book: BookIn,
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
) -> BookOut | None:
    inserted = await book_col.insert_one(dict(book))
    return await book_col.find_one(inserted.inserted_id)


@router.get("/")
async def get_books(
    params: Annotated[PagingParams, Depends(paging_params)],
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
) -> list[BookOut]:
    cursor = book_col.find().skip(params.skip).limit(params.limit)
    return await cursor.to_list(params.limit)


@router.get("/{id}")
async def get_book(id: str, book_col: AsyncIOMotorCollection = Depends(get_book_collection)) -> BookOut:
    book = await book_col.find_one({"_id": ObjectId(id)})

    if book is None:
        raise HTTPException(detail="Book not found", status_code=404)
    
    return book


@router.get("/findByTitle/{title}")
async def get_book_by_title(
    title: str,
    params: Annotated[PagingParams, Depends(paging_params)],
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
) -> list[BookOut]:
    cursor = book_col.find({"title": {"$regex": title}}).skip(params.skip).limit(params.limit)
    return await cursor.to_list(params.limit)


@router.get("/findByAuthor/{author}")
async def get_book_by_author(
    author: str,
    params: Annotated[PagingParams, Depends(paging_params)],
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
) -> list[BookOut]:
    cursor = book_col.find({"author": {"$regex": author}}).skip(params.skip).limit(params.limit)
    return await cursor.to_list(params.limit)


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_book(
    id: str,
    book: BookIn,
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
) -> BookOut:
    db_book = await book_col.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(book)})

    if db_book is None:
        raise HTTPException(detail="Book not found", status_code=404)
    
    return db_book


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_book(
    id: str,
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
):
    await book_col.delete_one({"_id": ObjectId(id)})
