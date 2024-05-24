
from typing import List
from datetime import datetime
from pydantic import BaseModel

# Bro
class BroModel(BaseModel):
    bro_id: str
    name: str
    email: str


# Exercise
class ExerciseModel(BaseModel):
    name: str
    sets: int
    reps: int
    weight: float

"""
# TODO: 
    Exercise design problems:
    - No weight
    - Various number of reps and weight for each set
        - Might have to have a set model that does reps, weights, etc.
    - Maybe store exercises as well?
"""


# Workout
class WorkoutModel(BaseModel):
    workout_id: str
    date: datetime
    bro_id: str
    exercises: List[ExerciseModel]



class User(BaseModel):
    username: str
    password: str