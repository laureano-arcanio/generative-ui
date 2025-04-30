from datetime import datetime

from pydantic import EmailStr, Field, model_validator
from app.types.base import BaseAPISchema
from typing_extensions import Self
from app.types.enum.user_enum import UserRolesEnum

class UserOptional(BaseAPISchema):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    role: UserRolesEnum = UserRolesEnum.user
    created_at: datetime | None = None
    updated_at: datetime | None = None



class UserBase(UserOptional):
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRolesEnum = UserRolesEnum.user


class UserCreate(UserBase):
    password: str | None = Field(default=None, exclude=True)


class UserUpdate(UserOptional):
    id : str | None = Field(default=None, exclude=True)
    updated_at: datetime | None = Field(default_factory=datetime.utcnow)
    created_at: datetime | None = Field(default=None, exclude=True)


    @model_validator(mode="after")
    def nullify_protected_attributes(self) -> Self:
        """Ensure protected attributes are nullified during update.

        Prevents modification of created_at and updated_at timestamps
        which are managed by the database.

        Returns:
            Self: The validated model instance with protected attributes nullified
        """
        self.created_at = None
        self.updated_at = None
        return self


class UserDetail(UserBase):
    pass

class UserDetailList(UserBase):
    pass