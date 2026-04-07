from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

load_dotenv() # Load environment variables from .env file

DATABASE_URL = os.getenv("dburl") 
engine = create_engine(DATABASE_URL) # Create a database engine using the URL from the environment variable

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is an API for the database management system. Please refer to the documentation for available endpoints."}

@app.get("/users")
async def get_users():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM users"))
        users = [dict(row) for row in result]
    return {"users": users}