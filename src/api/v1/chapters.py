from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.models.chapter import ChapterOut, ChapterIn
from src.models.common import PyObjectId
from src.structure import chapter_repository

router = APIRouter(prefix="/chapters", tags=["chapters"])


@router.post("/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_chapter(chapter: ChapterIn) -> ChapterOut | None:
    return await chapter_repository.create(chapter)


@router.get("/findByBookId/{id}")
async def get_book_chapters(
    id: PyObjectId,
    params: Annotated[PagingParams, Depends(paging_params)]
) -> list[ChapterOut]:
    return await chapter_repository.get_by_book(id, params)


@router.get("/{id}")
async def get_chapter(id: PyObjectId) -> ChapterOut:
    chapter = await chapter_repository.get_by_id(id)

    if chapter is None:
        raise HTTPException(detail="Chapter not found", status_code=404)
    
    return chapter


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_chapter(id: PyObjectId, chapter: ChapterIn) -> ChapterOut:
    db_chapter = await chapter_repository.update(id, chapter)

    if db_chapter is None:
        raise HTTPException(detail="Chapter not found", status_code=404)
    
    return db_chapter


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_chapter(id: PyObjectId):
    await chapter_repository.delete(id)
