
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


# Bro
class BroModel(BaseModel):
    bro_id: str
    name: str
    email: str


# Exercise
class ExerciseModel(BaseModel):
    name: str = Field(description="Name of the exercise", min_length=1)
    sets: int = Field(description="Number of sets performed", min_length=1)
    reps: int = Field(description="Number of reps performed", min_length=1)
    weight: float = Field(description="Weight used for the exercise, e.g. 60kg = 60", min_length=1)
    unit: str = Field(description="unit of measurement for the wight, e.g. 60kg = kg")

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


class ChatMessage(BaseModel):
    chat_message: str