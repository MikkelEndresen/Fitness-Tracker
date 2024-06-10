
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

# Great resource: https://fastapi.tiangolo.com/tutorial/sql-databases/

Base = declarative_base()

# # Define database model
# class User(Base):
#     __tablename__ = 'users' # The __tablename__ attribute tells SQLAlchemy the name of the table to use in the database for each of these models.
#     user_id = Column(Integer, primary_key=True)
#     username = Column(String, unique=True)
#     email = Column(String, unique=True)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
