#Session class to talk to the database in a safe and structured way.
# Session class is a middle man between python and your database
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

def create_user(db:Session,user:UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user) # add the user to the current session
    db.commit() #save all changes
    db.refresh(db_user) # updates your db_usr python object with the latest data from the database
    return db_user