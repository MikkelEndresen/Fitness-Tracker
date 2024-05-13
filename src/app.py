from fastapi import FastAPI

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

import os
import json

app = FastAPI()

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
    db = client.get_database("sample_mflix")


@app.on_event("shutdown")
async def shutdown_event():

    # Shutdown DB

    global db
    if db:
        await db.client.close()  # Close the MongoDB client connection
        print("MongoDB client connection closed.")

    

# Define your FastAPI routes and methods below
@app.get("/")
async def read_root():
    movies = db.get_collection("movies")
    # Query for a movie that has the title 'Back to the Future'
    query = { "title": "Back to the Future" }
    movie = await movies.find_one(query)
    return {"message": str(movie)}


