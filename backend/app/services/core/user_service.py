import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from app.types.user import UserBase, UserCreate
# from app.types.enum.user_enum import UserRolesEnum
# from datetime import datetime
from app.repositories.user_repository import UserRepository

logger = structlog.stdlib.get_logger(__name__)


class UserService:
    """Service class for managing user-related operations.

    This service handles CRUD operations for users.
    """

    def __init__(self, db_session: AsyncSession):
        """Initialize UserService with database session and required repositories.

        Args:
            db_session (AsyncSession): SQLAlchemy async database session
        """
        self.db_session = db_session
        self.user_repository = UserRepository(db_session)

    async def create_user(self, create_user: UserCreate) -> UserBase:
        """Retrieve all users.
        """
        user_without_password = UserCreate(**create_user.model_dump())

        return await self.user_repository.create(user_without_password)
