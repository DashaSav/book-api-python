from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.auth.jwt_bearer import JWTBearer
from src.models.common import PyObjectId
from src.models.rating import RatingIn, RatingOut
from src.structure import rating_repository

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.get("/findByBook/{book_id}")
async def get_ratings_by_book(book_id: PyObjectId) -> list[RatingOut]:
    rating = await rating_repository.get_by_book(book_id)

    if len(rating) == 0:
        raise HTTPException(detail="Ratings not found", status_code=404)
    
    return rating


@router.get("/findByUserAndBook/{user_id}/{book_id}")
async def get_rating_by_user_and_book(user_id: PyObjectId, book_id: PyObjectId) -> RatingOut | None:
    rating = await rating_repository.get_by_user_and_book(user_id, book_id)

    if not rating:
        raise HTTPException(detail="Rating not found", status_code=404)
    
    return rating


@router.post("/", dependencies=[Depends(JWTBearer())])
async def create_or_update_rating(rating: RatingIn) -> RatingOut:
    created_rating = await rating_repository.upsert(rating)

    if not created_rating:
       raise HTTPException(status_code=404)

    return created_rating


@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def get_rating(id: PyObjectId) -> RatingOut:
    rating = await rating_repository.get_by_id(id)

    if rating is None:
        raise HTTPException(detail="Rating not found", status_code=404)
    
    return rating


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_rating(id: PyObjectId):
    await rating_repository.delete(id)
