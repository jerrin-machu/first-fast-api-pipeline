from sqlalchemy import Column,Integer,String
from app.database import Base

#user represent a database table

# This tells sqlalchemy "This class maps to a databse table."
class User(Base):
    __tablename__ = "users"
    # name of the table in the database that this model(User) maps to
    id = Column(Integer,primary_key=True, index=True)
    name= Column(String,index=True)
    email= Column(String,unique=True,index=True)


