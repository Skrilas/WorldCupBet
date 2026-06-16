from pydantic import BaseModel

class ApiTime(BaseModel):
    id: int
    nome: str