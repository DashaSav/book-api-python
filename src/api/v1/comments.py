from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.models.comment import CommentOut, CommentIn
from src.models.common import PyObjectId
from src.structure import comment_repository

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_comment(comment: CommentIn) -> CommentOut | None:
    return await comment_repository.create(comment)


@router.get("/findByBookId/{id}")
async def get_book_comments(
    id: PyObjectId,
    params: Annotated[PagingParams, Depends(paging_params)]
) -> list[CommentOut]:
    return await comment_repository.get_by_book(id, params)


@router.get("/findByUser/{user_id}")
async def get_user_comments(
    user_id: PyObjectId,
    params: Annotated[PagingParams, Depends(paging_params)]
) -> list[CommentOut]:
    return await comment_repository.get_by_user(user_id, params)


@router.get("/{id}")
async def get_comment(id: PyObjectId) -> CommentOut:
    comment = await comment_repository.get_by_id(id)

    if comment is None:
        raise HTTPException(detail="Comment not found", status_code=404)
    
    return comment


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_comment(id: PyObjectId, comment: CommentIn) -> CommentOut:
    db_comment = await comment_repository.update(id, comment)

    if db_comment is None:
        raise HTTPException(detail="Comment not found", status_code=404)
    
    return db_comment


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_comment(id: PyObjectId):
    await comment_repository.delete(id)
