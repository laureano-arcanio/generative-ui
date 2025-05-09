from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies.auth import get_current_user
from app.config import settings
from app.routers import user_router, auth_router, generative_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix=settings.API_V1_STR, dependencies=[Depends(get_current_user)])
app.include_router(auth_router.router, prefix=settings.API_V1_STR)
app.include_router(generative_router.router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"health": "ok"}
