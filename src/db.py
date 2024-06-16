from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from . import models

def getSession():
    # Define database engine
    engine = create_engine('postgresql://postgres:Snig#eRdoodle456hah@localhost:5433/testex')

    # Define Base class for declarative models
    Base = declarative_base()
    
    models.Base.metadata.create_all(engine)

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session