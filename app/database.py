from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from tenacity import retry, wait_fixed, stop_after_attempt
import time
import os
from dotenv import load_dotenv
# loads environment variables from a .env file into your Python program.
load_dotenv()
DB_USER = os.getenv("POSTGRES_USER","postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD","my-secretpassword")
DB_HOST = os.getenv("DB_HOST","localhost")
DB_PORT = os.getenv("DB_PORT",5432)
DB_NAME = os.getenv("POSTGRES_DB","postgres")

SQLALCHEMY_DATABASE_URL = (f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")










#creating a sqlalchemy engine that connects to the database specified by the database url
# knows how to connect to the database
# manages connections
# executing sql
# Transactions.
@retry(wait=wait_fixed(2), stop=stop_after_attempt(10))
def get_engine():

    return create_engine(SQLALCHEMY_DATABASE_URL)
engine = get_engine()
# returns a class or a factory to create a new Session objects
# interacts with database
# performing crud operations
# Manage transactions.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# it tells sqlalchemy : "These classes are linked to tables in database."

Base = declarative_base()

