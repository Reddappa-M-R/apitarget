from pydantic import BaseModel

class ApiTarget(BaseModel):
    userId: int
    id: int
    title: str
    body: str
