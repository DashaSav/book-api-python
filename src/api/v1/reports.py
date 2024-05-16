from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.models.common import PyObjectId
from src.models.report import BookReportIn, BookReportOut, UserReportIn, UserReportOut
from src.structure import user_report_repository, book_report_repository

router = APIRouter(prefix="/reports", tags=["reports"])


# region users
@router.get("/users", dependencies=[Depends(JWTBearer())])
async def get_user_reports(params: Annotated[PagingParams, Depends(paging_params)]) -> list[UserReportOut]:
    report = await user_report_repository.get_all(params)

    if len(report) == 0:
        raise HTTPException(detail="Reports not found", status_code=404)
    
    return report


@router.post("/users", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_user_report(report: UserReportIn) -> UserReportOut:
    created_report = await user_report_repository.create(report)

    if not created_report:
       raise HTTPException(status_code=404)

    return created_report


@router.get("/users/{id}", dependencies=[Depends(JWTBearer())])
async def get_user_report(id: PyObjectId) -> UserReportOut:
    report = await user_report_repository.get_by_id(id)

    if report is None:
        raise HTTPException(detail="Report not found", status_code=404)
    
    return report


@router.put("/users/{id}", dependencies=[Depends(JWTBearer())])
async def update_user_report(id: PyObjectId, report: UserReportIn) -> UserReportOut:
    updated_report = await user_report_repository.update(id, report)

    if not updated_report:
        raise HTTPException(detail="Report not found", status_code=404)
    
    return updated_report


@router.delete("/users/{id}", dependencies=[Depends(JWTBearer())])
async def delete_user_report(id: PyObjectId):
    await user_report_repository.delete(id)
# endregion


# region books
@router.get("/books", dependencies=[Depends(JWTBearer())])
async def get_book_reports(params: Annotated[PagingParams, Depends(paging_params)]) -> list[BookReportOut]:
    report = await book_report_repository.get_all(params)

    if len(report) == 0:
        raise HTTPException(detail="Reports not found", status_code=404)
    
    return report


@router.post("/books", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_book_report(report: BookReportIn) -> BookReportOut:
    created_report = await book_report_repository.create(report)

    if not created_report:
       raise HTTPException(status_code=404)

    return created_report


@router.get("/books/{id}", dependencies=[Depends(JWTBearer())])
async def get_book_report(id: PyObjectId) -> BookReportOut:
    report = await book_report_repository.get_by_id(id)

    if report is None:
        raise HTTPException(detail="Report not found", status_code=404)
    
    return report


@router.put("/books/{id}", dependencies=[Depends(JWTBearer())])
async def update_book_report(id: PyObjectId, report: BookReportIn) -> BookReportOut:
    updated_report = await book_report_repository.update(id, report)

    if not updated_report:
        raise HTTPException(detail="Report not found", status_code=404)
    
    return updated_report


@router.delete("/books/{id}", dependencies=[Depends(JWTBearer())])
async def delete_book_report(id: PyObjectId):
    await book_report_repository.delete(id)
# endregion
