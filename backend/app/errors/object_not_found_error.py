from fastapi import Request, status
from fastapi.responses import JSONResponse


class ObjectNotFoundError(Exception):
    """Exception raised when a requested object cannot be found in the database.

    Args:
        object_type (str): The type of object that was not found
        object_id (int): The ID of the object that was not found
    """

    def __init__(self, object_type: str, object_id: int):
        self.object_type = object_type
        self.object_id = object_id
        self.message = f"{object_type} with id {object_id} not found"


async def object_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle ObjectNotFoundError exceptions by returning an appropriate JSON response.

    Args:
        request (Request): The incoming request
        exc (Exception): The exception that was raised

    Returns:
        JSONResponse: Response with 404 status code for ObjectNotFoundError or 500 for other exceptions
    """
    if isinstance(exc, ObjectNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )
    else:
        # Handle other exceptions if needed
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "An unexpected error occurred - invalid exception handler"
            },
        )
