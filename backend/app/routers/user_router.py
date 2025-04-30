from fastapi import APIRouter

from app.dependencies.services import UserServiceDependency
from app.types.user import UserBase, UserCreate

router = APIRouter(prefix="/v1/user", tags=["user"])


@router.post("/", response_model=UserBase, status_code=201)
async def create_user(user_create: UserCreate, userService: UserServiceDependency) -> UserBase:


    return await userService.create_user(user_create)
