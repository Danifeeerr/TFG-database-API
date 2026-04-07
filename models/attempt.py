from pydantic import BaseModel
from datetime import time, datetime

class Attempt(BaseModel):
    userid: int
    trainingid: int
    time_spent: time
    number_errors: int
    timestamp: datetime

