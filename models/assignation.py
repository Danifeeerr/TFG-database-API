from pydantic import BaseModel
from datetime import date

class Assignation(BaseModel):
    userid: int
    trainingid: int
    completed: bool
    date: date

class AssignationInsert(BaseModel):
    userid: int
    trainingid: int
    date: date

class AssignationUpdate(BaseModel):
    userid: str
    trainingid: int
    completed: bool