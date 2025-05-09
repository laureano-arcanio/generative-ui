from app.types.base import BaseAPISchema

class GenerativeCreate(BaseAPISchema):
    user_prefferences: str = ""
    persona_id: int = 1
    designer_id: int = 1

class GenerativeDetail(GenerativeCreate):
    user_prefferences: str
    raw_component: str = ""
    persona_id: int = 1
    designer_id: int = 1
    generated_prompt: str = ""  # New field to store the generated prompt

