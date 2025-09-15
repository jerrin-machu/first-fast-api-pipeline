#using pydantic to define data validation schemAS
#Structured data models with automatic Validation, Parsing, Error handling, Do
from pydantic import BaseModel

# validating name and email are present and are strings
class UserCreate(BaseModel):
    name:str
    email:str
# This creates a new Pydantic model that, inherits everything from userCreate (so it has already has name and email) # adds an id field(integer)
# this model is used for response. The id comes from the database, not from the user input,  so you did not include it in the userCreate
class UserOut(UserCreate):
    id:int

    class Config:
        orm_mode = True

    #  This tells pydantic that the data might come from ORM objects, not jsut plain dicts