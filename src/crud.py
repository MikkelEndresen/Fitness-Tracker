
# Create, Read, Update, Delete

from sqlalchemy.orm import Session
from . import models
from . import schemas
from datetime import date

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, password: str):
    db_user = models.User(username=username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    db_exercise = models.Exercise(**exercise.model_dump())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

def create_workout(db: Session, workout: schemas.WorkoutCreate):
    db_workout = models.Workout(**workout.model_dump())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

def get_workout_by_date(db: Session, date_in: date):
    return db.query(models.Workout).filter(models.Workout.date == date_in).first()
