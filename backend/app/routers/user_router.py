from fastapi import APIRouter

from app.dependencies.services import UserServiceDependency
from app.types.user import UserBase, UserCreate, UserDetail
from app.dependencies.database import DatabaseSession


router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=list[UserDetail], status_code=201)
async def get_users(userService: UserServiceDependency, db_session: DatabaseSession) -> list[UserDetail]:
    users = await userService.get_users()
    return users

@router.post("/", response_model=UserBase, status_code=201)
async def create_user(user_create: UserCreate, userService: UserServiceDependency, db_session: DatabaseSession) -> UserBase:
    user = await userService.create_user(user_create)
    await db_session.commit()
    return user
