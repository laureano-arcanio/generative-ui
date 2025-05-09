from typing import Annotated

from fastapi import Depends

from app.dependencies.database import DatabaseSession
from app.services.core.user_service import UserService
from app.services.core.generative import GenerativeService


def get_user_service(db_session: DatabaseSession) -> UserService:
    """Get a UserService instance with the provided database session.
        Args:
            db_session (DatabaseSession): The database session to use.

        Returns:
            UserService: An instance of UserService.
        """
    return UserService(db_session)

def get_generative_service() -> GenerativeService:
    """Get a UserService instance with the provided database session.
        Args:
            db_session (DatabaseSession): The database session to use.

        Returns:
            UserService: An instance of UserService.
        """
    return GenerativeService()

# FastAPI dependency annotations
UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
"""FastAPI dependency for injecting CallService"""

GenerativeServiceDependency = Annotated[GenerativeService, Depends(get_generative_service)]
"""FastAPI dependency for injecting GenerativeService"""
