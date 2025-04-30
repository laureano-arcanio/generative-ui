"""
Database models for the Tempus application.

This module defines the SQLAlchemy ORM models that represent the database schema.
It includes an abstract base class for common model attributes and imports all
model classes to make them available through the models package.
"""

from sqlalchemy import (
    Column,
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """
    Base declarative class for SQLAlchemy models.

    This class serves as the foundation for all database models in the application,
    providing SQLAlchemy's declarative model functionality.
    """

    pass


class AbstractBase(Base):
    """
    Abstract base class providing common primary key and timestamp fields for all models.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    """Primary key for the model"""

    created_at = Column(DateTime(timezone=True), default=func.now())
    """Timestamp when the record was created"""

    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    """Timestamp when the record was last updated"""


from .user_model import User  # noqa

__all__ = [
    "User",
]
