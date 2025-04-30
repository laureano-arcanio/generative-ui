from typing import Annotated

from fastapi import Depends

from app.dependencies.database import DatabaseSession
from app.services.core.user_service import UserService


def get_user_service(db_session: DatabaseSession) -> UserService:

    return UserService(db_session)



# FastAPI dependency annotations
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
"""FastAPI dependency for injecting CallService"""
