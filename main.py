from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError,NoResultFound
import os
from typing import List

from models.users import Users, UsersInsert

load_dotenv() # Load environment variables from .env file

DATABASE_URL = os.getenv("dburl") 
engine = create_engine(DATABASE_URL) # Create a database engine using the URL from the environment variable

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is an API for the database management system. Please refer to the documentation for available endpoints."}

 ###########################################################
 ##########################USERS############################
 ###########################################################

@app.get("/users", response_model=List[Users], tags=["Users"])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users")).fetchall()
    users = [{"id": r[0], "username": r[1], "password_hash": r[2],"admin": r[3]} for r in result]
    return users


@app.get("/user/{id}", response_model=Users, tags=["Users"])
def get_user_by_id(id: int):
    with engine.connect() as conn:
        res = conn.execute(
            text("SELECT * FROM users where id= :id"), 
            {"id": id}
        ).mappings().first()

        if res is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return res

 
@app.post("/users/new", response_model=Users, tags=["Users"])
def create_new_user(u: UsersInsert):
    with engine.connect() as conn:
        try:
            user = conn.execute(
                text("INSERT INTO users (username, password_hash, admin) VALUES (:username, :pass, :admin) RETURNING *"),
                {"username": u.username, 
                 "pass": u.password_hash, 
                 "admin": u.admin}
            ).mappings().one()

            conn.commit()
            return user
        
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Username already exists")
        

@app.post("/users/update", response_model=Users, tags=["Users"])
def update_user(u: Users):
    with engine.connect() as conn:
        try:
            user = conn.execute(
                text("UPDATE users SET username = :username, password_hash = :pass, admin = :admin WHERE id = :id RETURNING *"),
                {"username": u.username,
                 "pass": u.password_hash,
                 "admin": u.admin,
                 "id": u.id}
            ).mappings().one()

            conn.commit()

            return user
        
        except NoResultFound:
            raise HTTPException(status_code=404, detail="User not found")             
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Username already exists")
        
@app.delete("/users/delete/{id}", tags=["Users"])
def delete_user(id: int):
    with engine.connect() as conn:
        res = conn.execute(
            text("DELETE FROM users where id = :id RETURNING *"),
            {"id": id}
        ).mappings().first()
        conn.commit()

        if res is None:
            raise HTTPException(status_code=404, detail="User not found")
    
        return res

    
 ###########################################################
 ##########################TRAINING#########################
 ###########################################################

