from pydantic import BaseModel

class Target(BaseModel):
    userId: int
    id: int
    title: str
    body: str
