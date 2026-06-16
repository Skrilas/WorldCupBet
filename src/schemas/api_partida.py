from requests import request
from pydantic import BaseModel

class ApiPartida(BaseModel):
    id: int | None