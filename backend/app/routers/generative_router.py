from fastapi import APIRouter

from app.dependencies.services import UserServiceDependency, GenerativeServiceDependency
from app.types.generative import GenerativeCreate, GenerativeDetail
from app.dependencies.database import DatabaseSession


router = APIRouter(prefix="/generative", tags=["Generative components"])


@router.post("/react", response_model=GenerativeDetail, status_code=201)
async def get_generative(generativeService: GenerativeServiceDependency, generative_create: GenerativeCreate) -> GenerativeDetail:
    users = await generativeService.build_generative_component(
        generative_schema=generative_create
    )
    return users

