from pydantic import BaseModel

class ApiTime(BaseModel):
    id: int
    name_en: str