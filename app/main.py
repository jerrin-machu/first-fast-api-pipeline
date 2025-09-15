from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import database,models,schemas,crud
from app.schemas.user import UserCreate,UserOut
from app.crud.user import create_user as create_user_in_db


from app.database import Base

#Go look at all the model classes that inherit from Base, and create their
#corresponding tables in the database(if they don't already exist)

Base.metadata.create_all(bind=database.engine)

app = FastAPI()
#creates an object(app)that:
#knows how to handle HTTP requests.
#Lets you define API routes (GET,POST, Put, delete etc)
#can serve your app usingUVicorn or other Asgi servers

def get_db():
    db = database.SessionLocal()
    # This line creates a new database session that you can use to :
    # Query data from the database
    # insert new rows
    # Commit transactions
    # Rollback if needed.
    try:
        yield db #give the db session to FastAPi and pause
    finally:
        db.close() # after route is done close the connection.
@app.post("/users",response_model= UserOut)
#"When someone sends a post request to /users/, call the function below, and return the response in the shape of schemas.User"
def create_user_end_point(user:UserCreate,db:Session=Depends(get_db)):

    return create_user_in_db(db=db,user=user)
# when someone sends a post request to "/users with json body, validatet he input, create a new databse session, and call the logic that inserts the user into the databas. then return the newly created user"