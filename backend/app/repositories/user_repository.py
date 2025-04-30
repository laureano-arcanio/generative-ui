import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User

from app.repositories.base_repository import BaseRepository
from app.types.user import (
    UserBase,
    UserCreate,
    UserDetail,
    UserUpdate,
    UserDetailList
)

logger = structlog.stdlib.get_logger(__name__)


class UserRepository(
    BaseRepository[
        User,
        UserBase,
        UserDetail,
        UserDetailList,
        UserCreate,
        UserUpdate,
    ]
):
    """
    """

    model = User
    """The CaUserll SQLAlchemy model class"""

    base_schema = UserBase
    """UserBase schema for basic operations"""

    detail_schema = UserDetail
    """UserDetail schema for detailed view"""

    list_schema = UserDetailList
    """UserDetail schema for list operations"""

    detail_options = []
    """SQLAlchemy load options for detailed queries"""

    list_options = []
    """Load options for list queries"""
    
    async def get_by_email(self, email: str) -> UserBase | None:
        """Retrieve a user by their email address.
        
        Args:
            email: The email address to look up
            
        Returns:
            UserBase: The user if found, None otherwise
        """
        query = select(self.model).where(self.model.email == email)
        result = await self.db_session.execute(query)
        user = result.scalars().first()
        
        if not user:
            return None
            
        return self.base_schema.model_validate(user)


