from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption
from sqlalchemy.sql.expression import UnaryExpression

from app.errors import ObjectNotFoundError
from app.models import AbstractBase
from app.types.base import BaseAPISchema

# Type variables for generic type hints
ModelType = TypeVar("ModelType", bound=AbstractBase)
BaseSchemaType = TypeVar("BaseSchemaType", bound=BaseAPISchema)
DetailSchemaType = TypeVar("DetailSchemaType", bound=BaseAPISchema)
ListSchemaType = TypeVar("ListSchemaType", bound=BaseAPISchema)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseAPISchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseAPISchema)


class BaseRepository(
    Generic[
        ModelType,
        BaseSchemaType,
        DetailSchemaType,
        ListSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    """
    Generic base repository implementing common CRUD operations on SQLAlchemy models.

    This class provides a template for creating repositories for specific models
    while maintaining type safety through generic types. It handles basic database
    operations and schema validation.


    The repository pattern abstracts database operations and provides a consistent
    interface for working with different models while maintaining separation of concerns.

    Type Parameters:
        ModelType: The SQLAlchemy model type
        BaseSchemaType: The base Pydantic schema type for the model
        DetailSchemaType: The detailed Pydantic schema type for single instance retrieval
        ListSchemaType: The Pydantic schema type for list operations
        CreateSchemaType: The Pydantic schema type for create operations
        UpdateSchemaType: The Pydantic schema type for update operations
    """

    model: type[ModelType]
    """The SQLAlchemy model class for the repository"""

    base_schema: type[BaseSchemaType]
    """The base Pydantic schema class for the model"""

    detail_schema: type[DetailSchemaType]
    """The detailed Pydantic schema class for single instance retrieval"""

    detail_options: list[ExecutableOption] = []
    """List of SQLAlchemy options for detailed queries"""

    list_schema: type[ListSchemaType]
    """The Pydantic schema class for list operations"""

    list_options: list[ExecutableOption] = []
    """List of SQLAlchemy options for list queries"""

    list_order: list[UnaryExpression[Any]] = []
    """List of SQLAlchemy expressions for ordering list results"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def _get_db_instance_by_id(
        self, id: int, options: list[ExecutableOption] | None = None
    ) -> ModelType:
        """
        Retrieve a database instance by its ID.

        Args:
            id: The ID of the instance to retrieve
            options: Optional list of SQLAlchemy query options

        Returns:
            The model instance

        Raises:
            ObjectNotFoundError: If no instance is found with the given ID
        """
        if options:
            query = select(self.model).where(self.model.id == id).options(*options)
        else:
            query = select(self.model).where(self.model.id == id)
        result = await self.db_session.execute(query)
        db_instance = result.scalar_one_or_none()
        if not db_instance:
            raise ObjectNotFoundError(object_type=self.model.__name__, object_id=id)
        return db_instance

    async def get_all(
        self, options: list[ExecutableOption] | None = None
    ) -> list[ListSchemaType]:
        """
        Retrieve all instances of the model.

        Args:
            options: Optional list of SQLAlchemy query options to override defaults

        Returns:
            List of instances converted to list schema type
        """
        query = select(self.model)
        if options:
            query = query.options(*options)
        else:
            query = query.options(*self.list_options)

        if self.list_order:
            query = query.order_by(*self.list_order)

        result = await self.db_session.execute(query)
        instances = result.scalars().all()
        return [self.list_schema.model_validate(instance) for instance in instances]

    async def create(self, create_schema: CreateSchemaType) -> BaseSchemaType:
        """
        Create a new instance of the model.

        Args:
            create_schema: The validated create schema containing the data

        Returns:
            The created instance converted to base schema type
        """
        db_instance = self.model(**create_schema.model_dump())
        self.db_session.add(db_instance)
        await self.db_session.flush()
        return self.base_schema.model_validate(db_instance)

    async def get_by_id(
        self, id: int, options: list[ExecutableOption] | None = None
    ) -> DetailSchemaType:
        """
        Retrieve a single instance by ID with optional query options.

        Args:
            id: The ID of the instance to retrieve
            options: Optional list of SQLAlchemy query options to override defaults

        Returns:
            The instance converted to detail schema type

        Raises:
            ObjectNotFoundError: If no instance is found with the given ID
        """
        db_instance = await self._get_db_instance_by_id(
            id, options=options or self.detail_options
        )
        return self.detail_schema.model_validate(db_instance)

    async def update(self, id: int, update_schema: UpdateSchemaType) -> BaseSchemaType:
        """
        Update an existing instance by ID.

        Args:
            id: The ID of the instance to update
            update_schema: The validated update schema containing the new data

        Returns:
            The updated instance converted to base schema type

        Raises:
            ObjectNotFoundError: If no instance is found with the given ID
        """
        db_instance = await self._get_db_instance_by_id(id)
        update_data = update_schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_instance, key, value)
        self.db_session.add(db_instance)
        await self.db_session.flush()
        await self.db_session.refresh(db_instance)
        return self.base_schema.model_validate(db_instance)

    async def delete(self, id: int) -> None:
        """
        Delete an instance by ID.

        Args:
            id: The ID of the instance to delete

        Raises:
            ObjectNotFoundError: If no instance is found with the given ID
        """
        db_instance = await self._get_db_instance_by_id(id)
        await self.db_session.delete(db_instance)
        await self.db_session.flush()
