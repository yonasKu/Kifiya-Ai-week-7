# database.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load the .env file
load_dotenv()

def get_connection():
    # Get environment variables
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    # Create the connection string
    connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    # Create the database engine
    engine = create_engine(connection_string)
    return engine

# Create the SQLAlchemy engine
engine = get_connection()

# Create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()
