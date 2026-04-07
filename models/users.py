from pydantic import BaseModel

class Users(BaseModel):
    id: int
    username: str
    password_hash: str
    admin: bool

class UsersInsert(BaseModel):
    username: str
    password_hash: str
    admin: bool
