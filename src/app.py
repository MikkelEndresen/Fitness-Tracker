from fastapi import FastAPI, Depends, HTTPException

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

import os
import json
import jwt
import bcrypt

from .schemas import ExerciseCreate, Exercise, ChatMessage, WorkoutCreate
from .utils import verify_token, token_to_user
from .llm import prompt_model

from .db import getSession
from . import crud, schemas
from datetime import date

from sqlalchemy.orm import Session


# HEY!
# uvicorn src.app:app --reload

# JWT setup #TODO: hide this
SECRET_KEY = "banana-apple-smoothie"
ALGORITHM = "HS256"

app = FastAPI() # uvicorn app:app --reload

# get config file
config_file = open("config/config.json", "r")
config = json.load(config_file)

db_session = getSession()

# Database 
db = None

def get_db():
    db = getSession()  # Replace SessionLocal() with your method to get the db_session
    try:
        yield db
    finally:
        db.close()

# Define a method to run on startup
@app.on_event("startup")    #new
async def startup_event():
    print("Server is starting up...")

    client = AsyncIOMotorClient(config['testcluster'])
    global db
    db = client.get_database('GymBro')

    print("Server started")


@app.on_event("shutdown")
async def shutdown_event():

    # Shutdown DB

    global db
    if db is not None:
        db.client.close() # Close the MongoDB client connection
        print("MongoDB client connection closed.")
    
# User registration
@app.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = crud.create_user(db, user.username, hashed_password)
    return {"message": "User registered successfully"}

# User login
@app.post("/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    hashed_password_bytes = bytes.fromhex(db_user.password.replace('\\x', ''))  # Convert hexadecimal string to bytes
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), hashed_password_bytes):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # Create token and return it
    token = jwt.encode({"username": db_user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}


# Protected route
@app.get("/protected")
async def protected(token: str = Depends(verify_token)):
    return {"message": "This is a protected route, but you are in the very special club my friend"}


@app.post("/record_exercise")
async def basic(msg: ChatMessage, token: str = Depends(verify_token), db: Session = Depends(get_db)):
    
    print("Accepted to /record_exercise")

    result = prompt_model(msg)

    # Check for current workout
    # global db
    # workout_collection = db['workouts']

    #workout = await workout_collection.find_one({'dateField': {'$exists': True, '$eq': str(date.today())}})
    workout = crud.get_workout_by_date(db, date.today())

    if workout is None:
        #user_collection = db['users']
        #user = await user_collection.find_one({"username": token_to_user(token)})
        user = crud.get_user_by_username(token_to_user(token))

        workout = WorkoutCreate(user = user.id, date = str(date.today()), exercises = [])
        workout_db = crud.create_workout(get_db, workout)
        #workout_collection.insert_one(workout.dict())

    print('-'*80)
    print(result)
    print('-'*80)
    exercise = Exercise(name=result['name'], sets=result['sets'], reps=result['reps'], weight=result['weight'], unit=result['unit'])
    exercise_db = crud.create_exercise(db, exercise)
    # exercise_dict = dict(exercise)
    # exercise_dict['workout'] = workout
    # db_exercise =  DbExerciseModel(**exercise_dict)

    workout_db.exercises.append(exercise_db)
    # Commit the changes to the database
    db.commit()

    #exercise_collection = db['exercise']

    #await exercise_collection.insert_one(db_exercise.dict())

    return {"message": "Fucking success that lad", "db item": exercise_db}


@app.post("/message/")
async def recieve_message(message: str):

    return {"message": message}

# @app.post("/test_db/")
# async def test_db(test: ExerciseModel):

#     global db
#     exercise_collection = db["exercise"]
#     await exercise_collection.insert_one(test.dict())

#     return {"message": "success"}


# Define your FastAPI routes and methods below
@app.get("/")
async def read_root():
    movies = db.get_collection("movies")
    # Query for a movie that has the title 'Back to the Future'
    query = { "title": "Back to the Future" }
    movie = await movies.find_one(query)
    return {"message": str(movie)}


