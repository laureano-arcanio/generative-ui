import structlog
from sqlalchemy import select

from app.models import User

from app.repositories.base_repository import BaseRepository
from app.types.user import (
    UserBase,
    UserCreate,
    UserDetail,
    UserUpdate,
)

logger = structlog.stdlib.get_logger(__name__)


class UserRepository(
    BaseRepository[
        User,
        UserBase,
        UserDetail,
        UserDetail,
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

    list_schema = UserDetail
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
        
        if user is None:
            return None

        return self.base_schema.model_validate(user)
    
    async def create_with_hashed_password(self, create_schema: UserCreate, hashed_password: str) -> UserBase:
        """
        Create a new instance of the model.

        Args:
            create_schema: The validated create schema containing the data

        Returns:
            The created instance converted to base schema type
        """
        db_instance = self.model(**create_schema.model_dump(), hashed_password=hashed_password)
        self.db_session.add(db_instance)
        await self.db_session.flush()
        return self.base_schema.model_validate(db_instance)


