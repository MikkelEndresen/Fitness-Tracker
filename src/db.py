from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from . import models

def getSession():
    # Define database engine
    engine = create_engine('postgresql://postgres:Snig#eRdoodle456hah@localhost:5433/gymbro')

    # Define Base class for declarative models
    Base = declarative_base()

    # # Define database model
    # class User(Base):
    #     __tablename__ = 'users' # The __tablename__ attribute tells SQLAlchemy the name of the table to use in the database for each of these models.
    #     user_id = Column(Integer, primary_key=True)
    #     username = Column(String, unique=True)
    #     email = Column(String, unique=True)

    # class Test(Base):
    #     __tablename__ = 'test'
    #     id = Column(Integer, primary_key = True)
    #     test = Column(String, unique=True)

    # Create database tables
    models.Base.metadata.create_all(engine)

    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Interact with database
    # Example: Insert a new user
    # new_user = User(username='john_doe', email='john@example.com')
    # session.add(new_user)
    # session.commit()

    # # Query users
    # users = session.query(User).all()
    # for user in users:
    #     print(user.username, user.email)

    # # Close session
    # session.close()
    return session