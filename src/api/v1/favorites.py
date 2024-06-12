from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.models.book import BookOut, BookWithUser
from src.models.common import PyObjectId
from src.models.favorite_author import FavoriteAuthorIn, FavoriteAuthorOut
from src.models.favorite_book import FavoriteBookIn, FavoriteBookOut
from src.structure import favorite_books_repository, favorite_authors_repository, favorites_interactor

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/books/{user_id}", dependencies=[Depends(JWTBearer())])
async def get_user_favorite_books(
    user_id: PyObjectId,
    params: Annotated[PagingParams, Depends(paging_params)],
) -> list[BookWithUser]:
    return await favorites_interactor.get_user_favorite_books(user_id, params)


@router.post("/books/", dependencies=[Depends(JWTBearer())])
async def create_user_favorite_book(book: FavoriteBookIn) -> FavoriteBookOut:
    created_book = await favorite_books_repository.create(book)

    if not created_book:
        raise HTTPException(404, "Error adding book to favorites")
    
    return created_book


@router.delete("/books/{user_id}/{book_id}", dependencies=[Depends(JWTBearer())])
async def delete_user_favorite_book(user_id: PyObjectId, book_id: PyObjectId):
    await favorite_books_repository.delete(user_id, book_id)
