from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.models.common import PyObjectId
from src.models.report import ReportIn, ReportOut
from src.structure import report_repository

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_reports(params: Annotated[PagingParams, Depends(paging_params)]) -> list[ReportOut]:
    report = await report_repository.get_all(params)

    if len(report) == 0:
        raise HTTPException(detail="Reports not found", status_code=404)
    
    return report


@router.post("/", status_code=201, dependencies=[Depends(JWTBearer())])
async def create_report(report: ReportIn) -> ReportOut:
    created_report = await report_repository.create(report)

    if not created_report:
       raise HTTPException(status_code=404)

    return created_report


@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def get_report(id: PyObjectId) -> ReportOut:
    report = await report_repository.get_by_id(id)

    if report is None:
        raise HTTPException(detail="Report not found", status_code=404)
    
    return report


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_report(id: PyObjectId, report: ReportIn) -> ReportOut:
    updated_report = await report_repository.update(id, report)

    if not updated_report:
        raise HTTPException(detail="Report not found", status_code=404)
    
    return updated_report


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_report(id: PyObjectId):
    await report_repository.delete(id)
