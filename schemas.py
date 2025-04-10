from pydantic import BaseModel

class ApiTargetCreate(BaseModel):
    userId: int
    id: int
    title: str
    body: str