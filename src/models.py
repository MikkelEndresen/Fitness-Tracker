
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
import enum
from . import schemas


# Great resource: https://fastapi.tiangolo.com/tutorial/sql-databases/

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

# Define a workout
class Workout(Base):
    __tablename__  = 'workouts'

    workout_id = Column(Integer, primary_key=True)
    user_id = Column(Integer) # TODO add foreign key
    #user = relationship("User", back_populates="workouts")
    date = Column(Date, index=True)

    exercises = relationship("Exercise", back_populates="workout", cascade="all, delete-orphan")

class Exercise(Base):
    __tablename__ = 'exercises'

    exercise_id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    workout_id = Column(Integer, ForeignKey('workouts.workout_id'))

    workout = relationship("Workout", back_populates="exercises")


    