from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.dependencies.services import UserServiceDependency
from app.types.user import UserDetail

from app.dependencies.auth import login, get_current_user
from app.types.auth import Token


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: UserServiceDependency) -> Token:
    return await login(form_data, user_service)

@router.get("/me")
async def read_users_me(current_user: Annotated[UserDetail, Depends(get_current_user)]) -> UserDetail:
    return current_user