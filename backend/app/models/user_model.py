from . import AbstractBase
from sqlalchemy import String, Enum, Boolean
from sqlalchemy.orm import mapped_column
from app.types.enum.user_enum import UserRolesEnum


class User(AbstractBase):
    __tablename__ = "users"

    email = mapped_column(String, unique=True, index=True, nullable=False)
    first_name = mapped_column(String, nullable=False)
    last_name = mapped_column(String, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    active = mapped_column(Boolean, default=True, nullable=False)
    role = mapped_column(Enum(UserRolesEnum), default=UserRolesEnum.user, nullable=False)