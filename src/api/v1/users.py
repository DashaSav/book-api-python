from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from src.api.general import PagingParams, paging_params
from src.auth.jwt_bearer import JWTBearer
from src.models.auth import AuthRequest, AuthResponse
from src.models.common import PyObjectId
from src.models.user import UserIn, UserOut, UserUpdate
from src.structure import user_repository, user_interactor

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=201)
async def create_user(user: UserIn) -> AuthResponse:
    create_response = await user_interactor.create_user(user)

    if not create_response:
       raise HTTPException(status_code=404)

    return AuthResponse(user=create_response[0], token=create_response[1])


@router.post("/login")
async def login_user(request: AuthRequest) -> AuthResponse:
    auth_response = await user_interactor.login(request)

    if not auth_response:
       raise HTTPException(status_code=404)
    
    return AuthResponse(user=auth_response[0], token=auth_response[1])


@router.get("/{id}")
async def get_user(id: PyObjectId) -> UserOut:
    user = await user_repository.get_by_id(id)

    if user is None:
        raise HTTPException(detail="User not found", status_code=404)
    
    return user


@router.get("/findByEmail/{email}")
async def get_user_by_email(email: str) -> UserOut:
    user = await user_repository.get_by_email(email)
    if not user:
        raise HTTPException(detail="User not found", status_code=404)
    
    return user


@router.get("/findByName/{name}")
async def get_users_by_name(
    name: str,
    params: Annotated[PagingParams, Depends(paging_params)]
) -> list[UserOut]:
    users = await user_repository.get_by_name(name, params)
    if users.count is 0:
        raise HTTPException(detail="Users not found", status_code=404)
    
    return users


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_user(id: PyObjectId, user: UserUpdate) -> UserOut:
    updated_user = await user_interactor.update_user(id, user)
    if not updated_user:
        raise HTTPException(detail="User not found", status_code=404)
    
    return updated_user


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_user(id: PyObjectId):
    await user_repository.delete(id)
