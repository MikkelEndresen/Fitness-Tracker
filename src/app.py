from fastapi import FastAPI, Depends

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

import os
import json
import jwt
import bcrypt

from .schema import ExerciseModel, User, ChatMessage, WorkoutModel,  DbExerciseModel
from .utils import verify_token, token_to_user
from .llm import prompt_model

from datetime import date

# JWT setup #TODO: hide this
SECRET_KEY = "banana-apple-smoothie"
ALGORITHM = "HS256"

app = FastAPI() # uvicorn app:app --reload

# get config file
config_file = open("config/config.json", "r")
config = json.load(config_file)

# Database 
db = None

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
        db.client.close()  # Close the MongoDB client connection
        print("MongoDB client connection closed.")

# User registration
@app.post("/register")
async def register(user: User):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    
    global db
    user_collection = db["users"]
    await user_collection.insert_one({"username": user.username, "password": hashed_password})

    return {"message": "User registered successfully"}

# User login
@app.post("/login")
async def login(user: User):
    
    global db
    user_collection = db["users"]
    db_user = await user_collection.find_one({"username": user.username})

    if db_user and bcrypt.checkpw(user.password.encode("utf-8"), db_user["password"]):
        token = jwt.encode({"username": user.username}, SECRET_KEY, algorithm=ALGORITHM)
        return {"token": token}
    else:
        return {"message": "Invalid username or password"}


# Protected route
@app.get("/protected")
async def protected(token: str = Depends(verify_token)):
    return {"message": "This is a protected route, but you are in the very special club my friend"}


@app.post("/record_exercise")
async def basic(msg: ChatMessage, token: str = Depends(verify_token)):
    
    result = prompt_model(msg)

    # Check for current workout
    global db
    workout_collection = db['workouts']

    workout = await workout_collection.find_one({'dateField': {'$exists': True, '$eq': str(date.today())}})

    if workout is None:
        user_collection = db['users']
        user = await user_collection.find_one({"username": token_to_user(token)})
        
        workout = WorkoutModel(user = user, date = str(date.today()))
        workout_collection.insert_one(workout.dict())

    print('-'*80)
    print(result)
    print('-'*80)
    exercise = ExerciseModel(name=result['name'], sets=result['sets'], reps=result['reps'], weight=result['weight'], unit=result['unit'])

 
    exercise_dict = dict(exercise)
    exercise_dict['workout'] = workout
    db_exercise =  DbExerciseModel(**exercise_dict)

    exercise_collection = db['exercise']

    await exercise_collection.insert_one(db_exercise.dict())

    return {"message": "Fucking success that lad", "db item": db_exercise}


@app.post("/message/")
async def recieve_message(message: str):

    return {"message": message}

@app.post("/test_db/")
async def test_db(test: ExerciseModel):

    global db
    exercise_collection = db["exercise"]
    await exercise_collection.insert_one(test.dict())

    return {"message": "success"}


# Define your FastAPI routes and methods below
@app.get("/")
async def read_root():
    movies = db.get_collection("movies")
    # Query for a movie that has the title 'Back to the Future'
    query = { "title": "Back to the Future" }
    movie = await movies.find_one(query)
    return {"message": str(movie)}


