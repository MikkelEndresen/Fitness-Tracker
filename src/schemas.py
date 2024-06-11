
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


from datetime import datetime, date
from enum import Enum


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool

#     class Config:
#         orm_mode = True

class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str


class ChatMessage(BaseModel):
    chat_message: str

# Unit of measurement
class UnitEnum(str, Enum):
    kg = "kg"
    pounds = "lb"


class ExerciseBase(BaseModel):
    name: str = Field(description="Name of the exercise")

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    sets: int = Field(description="Number of sets performed")
    reps: int = Field(description="Number of reps performed")
    weight: float = Field(description="Weight used for the exercise, e.g. 60kg = 60")
    unit: UnitEnum = Field(description="Either kg or lb")

    class Config:
        orm_mode: True


class WorkoutBase(BaseModel):
    user: UserBase

class WorkoutCreate(WorkoutBase):
    exercises: List[ExerciseCreate]
    date: date

class Workout(WorkoutBase):
    id: int
    exercises: List[Exercise] = []

    class Config:
        orm_mode: True




"""
# TODO: 
    Exercise design problems:
    - No weight
    - Various number of reps and weight for each set
        - Might have to have a set model that does reps, weights, etc.
    - Maybe store exercises as well?
"""
