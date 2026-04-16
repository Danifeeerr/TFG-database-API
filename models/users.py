from pydantic import BaseModel
from typing import Optional 

class Users(BaseModel):
    id: int
    username: str
    password_hash: Optional[str] = None
    admin: bool

class UsersInsert(BaseModel):
    username: str
    password_hash: str
    admin: bool

class UserLogin(BaseModel):
    username: str
    password: str

    