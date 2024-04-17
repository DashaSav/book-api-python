from typing import Annotated
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.db import get_book_collection
from src.models.book import BookOut, BookIn
from src.serializers.book import to_book_out, to_books_out


router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_book(
    book: BookIn,
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
):
    inserted = await book_col.insert_one(dict(book))

    return BookOut(
        _id=str(inserted.inserted_id), 
        title=book.title,
        author=book.author, 
        description=book.description
    )


@router.get("/{id}")
async def get_book(id: str, book_col: AsyncIOMotorCollection = Depends(get_book_collection)) -> BookOut:
    book = await book_col.find_one({"_id": ObjectId(id)})

    if book is None:
        raise HTTPException(detail="Book not found", status_code=404)
    
    return to_book_out(book)


@router.get("/findByTitle/{title}")
async def get_book_by_title(
    title: str,
    params: Annotated[PagingParams, Depends(paging_params)],
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
) -> list[BookOut]:
    cursor = book_col.find({"title": {"$regex": title}}).skip(params.skip).limit(params.limit)
    
    books = await cursor.to_list(params.limit)
    
    return to_books_out(books)


@router.get("/findByAuthor/{author}")
async def get_book_by_author(
    author: str,
    params: Annotated[PagingParams, Depends(paging_params)],
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
) -> list[BookOut]:
    cursor = book_col.find({"author": {"$regex": author}}).skip(params.skip).limit(params.limit)
    
    books = await cursor.to_list(params.limit)
    
    return to_books_out(books)


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_book(
    id: str,
    book: BookIn,
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
) -> BookOut:
    db_book = await book_col.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(book)})

    if db_book is None:
        raise HTTPException(detail="Book not found", status_code=404)
    
    return to_book_out(db_book)


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_book(
    id: str,
    book_col: AsyncIOMotorCollection = Depends(get_book_collection)
):
    await book_col.delete_one({"_id": ObjectId(id)})
