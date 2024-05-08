from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.models.common import PyObjectId
from src.models.chapter import ChapterIn, ChapterOut
from src.structure import chapter_repository

router = APIRouter(prefix="/chapters", tags=["chapters"])


@router.post("/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_chapter(chapter: ChapterIn) -> ChapterOut:
    created_chapter = await chapter_repository.create(chapter)

    if not created_chapter:
       raise HTTPException(status_code=404)

    return created_chapter


@router.get("/{id}")
async def get_chapter(id: PyObjectId) -> ChapterOut:
    chapter = await chapter_repository.get_by_id(id)

    if chapter is None:
        raise HTTPException(detail="Chapter not found", status_code=404)
    
    return chapter


@router.get("/findByBook/{id}")
async def get_chapter_by_book(
    id: PyObjectId,
    params: Annotated[PagingParams, Depends(paging_params)]
) -> list[ChapterOut]:
    chapters = await chapter_repository.get_by_book(id, params)

    if len(chapters) == 0:
        raise HTTPException(detail="Chapters not found", status_code=404)
    
    return chapters


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_chapter(id: PyObjectId, chapter: ChapterIn) -> ChapterOut:
    updated_chapter = await chapter_repository.update(id, chapter)

    if not updated_chapter:
        raise HTTPException(detail="Chapter not found", status_code=404)
    
    return updated_chapter


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_chapter(id: str):
    await chapter_repository.delete(id)
