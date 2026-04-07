from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError,NoResultFound
import os
from typing import List

from models.users import Users, UsersInsert
from models.training import Training, TrainingInsert
from models.assignation import Assignation, AssignationInsert, AssignationUpdate

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
        result = conn.execute(text("SELECT * FROM users")).mappings().all()
        return result


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


@app.get("/training", response_model=List[Training], tags=["Trainings"])
def get_trainings():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM training")).mappings().all()

        return res

@app.get("/training/{id}", response_model=Training, tags=["Trainings"])
def get_training_by_id(id: int):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM training WHERE id = :id"),
        {"id": id}
        ).mappings().first()

        if res is None:
            raise HTTPException(status_code=404, detail="Training not found")
    
        return res

@app.post("/training/new", response_model=Training, tags=["Trainings"])
def create_new_training(t: TrainingInsert):
    with engine.connect() as conn:
        try:
            training = conn.execute(
                text("INSERT INTO training (name, hours, error_limit) VALUES (:name, :hours, :e_l) RETURNING *"),
                {"name": t.name, 
                 "hours": t.hours, 
                 "e_l": t.error_limit}
            ).mappings().one()

            conn.commit()
            return training
        
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Training name already exists")
        
@app.post("/training/update", response_model=Training, tags=["Trainings"])
def update_user(t: Training):
    with engine.connect() as conn:
        try:
            training = conn.execute(
                text("UPDATE training SET name = :name, hours = :hours, error_limit = :e_l WHERE id = :id RETURNING *"),
                {"name": t.name,
                 "hours": t.hours,
                 "e_l": t.error_limit,
                 "id": t.id}
            ).mappings().one()

            conn.commit()

            return training
        
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Training not found")             
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Training name already exists")
        
@app.delete("/training/delete/{id}", tags=["Trainings"])
def delete_training(id: int):
    with engine.connect() as conn:
        res = conn.execute(
            text("DELETE FROM training where id = :id RETURNING *"),
            {"id": id}
        ).mappings().first()
        conn.commit()

        if res is None:
            raise HTTPException(status_code=404, detail="Training not found")
    
        return res


 ###########################################################
 ######################ASSIGNATIONS#########################
 ###########################################################


@app.get("/assignation", response_model=List[Assignation], tags=["Assignations"])
def get_assignation():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM assignation")).mappings().all()

        return res

@app.get("/assignation/{userid}", response_model=List[Assignation], tags=["Assignations"])
def get_assignation_by_id(userid: int):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT * FROM assignation WHERE userid = :userid"),
        {"userid": userid}
        ).mappings().all()

        if not res:
            raise HTTPException(status_code=404, detail="Assignations not found")
    
        return res
    

@app.post("/assignation/new", response_model=Assignation, tags=["Assignations"])
def create_new_assignation(a: AssignationInsert):
    with engine.connect() as conn:
        try:
            assignation = conn.execute(
                text("INSERT INTO assignation (userid, trainingid, date) VALUES (:userid, :trainingid, :date) RETURNING *"),
                {"userid": a.userid, 
                 "trainingid": a.trainingid, 
                 "date": a.date}
            ).mappings().one()

            conn.commit()
            return assignation
        
        except IntegrityError:
            raise HTTPException(status_code=409, detail="The user may already have an assignation to this training or the user or the training does not exist")
        

@app.post("/assignation/update", response_model=Assignation, tags=["Assignations"])
def update_assignation(a: AssignationUpdate):
    with engine.connect() as conn:
        try:
            assignation = conn.execute(
                text("UPDATE assignation SET completed = :completed WHERE userid = :userid and trainingid = :trainingid RETURNING *"),
                {"completed": a.completed,
                 "userid": a.userid,
                 "trainingid": a.trainingid}
            ).mappings().one()

            conn.commit()

            return assignation
        
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Assignation not found")            

@app.delete("/assignation/delete", tags=["Assignations"])
def delete_assignation(userid: int, trainingid: int):
    with engine.connect() as conn:
        res = conn.execute(
            text("DELETE FROM assignation where userid = :userid and trainingid = :trainingid RETURNING *"),
            {"userid": userid,
             "trainingid": trainingid}
        ).mappings().first()
        conn.commit()

        if res is None:
            raise HTTPException(status_code=404, detail="Assignation not found")
    
        return res
 

