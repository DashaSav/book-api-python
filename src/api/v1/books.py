from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.models.book import BookWithUser, BookIn
from src.models.common import PyObjectId
from src.structure import book_repository, book_interactor


router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_book(book: BookIn) -> BookWithUser | None:
    return await book_repository.create(book)


@router.get("/")
async def get_books(
    params: Annotated[PagingParams, Depends(paging_params)]
) -> list[BookWithUser] | None:
    return await book_repository.get_all(params)


@router.get("/rating/{id}")
async def get_book_rating(id: PyObjectId):
    return await book_interactor.get_rating(id)


@router.get("/{id}")
async def get_book(id: PyObjectId) -> BookWithUser:
    book = await book_repository.get_by_id(id)

    if book is None:
        raise HTTPException(detail="Book not found", status_code=404)
    
    return book


@router.get("/findByTitle/{title}")
async def get_books_by_title(
    title: str,
    params: Annotated[PagingParams, Depends(paging_params)]
) -> list[BookWithUser]:
    return await book_repository.get_by_title(title, params)


@router.get("/findByAuthor/{author}")
async def get_books_by_author(
    author: str,
    params: Annotated[PagingParams, Depends(paging_params)]
) -> list[BookWithUser]:
    return await book_repository.get_by_author(author, params)


@router.get("/findByUser/{id}")
async def get_books_by_user(
    id: PyObjectId,
    params: Annotated[PagingParams, Depends(paging_params)]
) -> list[BookWithUser]:
    return await book_repository.get_by_user(id, params)


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_book(id: PyObjectId, book: BookIn) -> BookWithUser:
    db_book = await book_repository.update(id, book)

    if db_book is None:
        raise HTTPException(detail="Book not found", status_code=404)
    
    return db_book


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_book(id: PyObjectId):
    await book_repository.delete(id)
