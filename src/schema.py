
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


from datetime import date





class User(BaseModel):
    username: str
    password: str


class ChatMessage(BaseModel):
    chat_message: str


# Workout
class WorkoutModel(BaseModel):
    user: User
    date: str

# Exercise
class ExerciseModel(BaseModel):
    name: str = Field(description="Name of the exercise")
    sets: int = Field(description="Number of sets performed")
    reps: int = Field(description="Number of reps performed")
    weight: float = Field(description="Weight used for the exercise, e.g. 60kg = 60")
    unit: str = Field(description="unit of measurement for the wight, e.g. 60kg = kg")

class DbExerciseModel(ExerciseModel):
    workout: Optional[WorkoutModel] = None


"""
# TODO: 
    Exercise design problems:
    - No weight
    - Various number of reps and weight for each set
        - Might have to have a set model that does reps, weights, etc.
    - Maybe store exercises as well?
"""
