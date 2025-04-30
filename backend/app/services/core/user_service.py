import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from app.types.user import UserBase, UserCreate
from app.repositories.user_repository import UserRepository
from passlib.context import CryptContext
from fastapi import HTTPException, status
logger = structlog.stdlib.get_logger(__name__)

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
        """Create a new user with hashed password.
        
        Args:
            create_user (UserCreate): User data including password
            
        Returns:
            UserBase: Created user without sensitive data
        """
        existing_user = await self.user_repository.get_by_email(create_user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
            
        # Hash the password
        user_data = create_user.model_dump(exclude={"password"})
        if create_user.password is None:
            raise ValueError("Password cannot be None")
        user_data["hashed_password"] = pwd_context.hash(create_user.password)
        
        # Create user with hashed password
        user_with_hashed_password = UserCreate(**user_data)
        
        return await self.user_repository.create(user_with_hashed_password)
