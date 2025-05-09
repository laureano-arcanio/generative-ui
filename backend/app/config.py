from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Backend"
    API_V1_STR: str = "/api/v1"

    AUTH_SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    AUTH_ALGORITHM: str = "HS256"
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OPEN_API_KEY: str = ""
    
    def get_database_url(self) -> str:
        """
        Get the database URL from environment variables.

        Returns:
            str: The database URL.

        Raises:
            ValueError: If the DATABASE_URL environment variable is not set.
        """
        database_url = os.getenv("DATABASE_URL")

        if database_url is None:
            raise ValueError("DATABASE_URL environment variable not set")

        return database_url
    
    def get_openai_api_key(self) -> str:
        """
        Get the OpenAI API key from environment variables.

        Returns:
            str: The OpenAI API key.

        Raises:
            ValueError: If the OPENAI_API_KEY environment variable is not set.
        """
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if openai_api_key is None:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        return openai_api_key
    

settings = Settings()