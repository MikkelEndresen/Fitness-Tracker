from sqlalchemy import create_engine, Column, Integer, String
#from sqlalchemy.ext.declarative import 
from sqlalchemy.orm import sessionmaker, declarative_base

# Define database engine
engine = create_engine('postgresql://postgres:Snig#eRdoodle456hah@localhost:5433/postgres')

# Define Base class for declarative models
Base = declarative_base()

# Define database model
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)

# Create database tables
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Interact with database
# Example: Insert a new user
new_user = User(username='john_doe', email='john@example.com')
session.add(new_user)
session.commit()

# Query users
users = session.query(User).all()
for user in users:
    print(user.username, user.email)

# Close session
session.close()