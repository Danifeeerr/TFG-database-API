from pydantic import BaseModel

class Training(BaseModel):
    id: int
    name: str
    hours: float
    error_limit: int

class TrainingInsert(BaseModel):
    name: str
    hours: float
    error_limit: int

