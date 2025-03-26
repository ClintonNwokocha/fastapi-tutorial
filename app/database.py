import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker                                                       
from .config import settings
import urllib.parse

#SQLAlchemy setup

encoded_password = urllib.parse.quote_plus(settings.database_password)
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{encoded_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Function to get DB session

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# Psycopg2 connection

def get_psycopg2_connection():
    while True:
        try:
            conn = psycopg2.connect(
                    host='localhost',
                    database='fastapi',
                    port=5433,
                    user='postgres',
                    password='@Odogwuguyman1',
                    cursor_factory=RealDictCursor
                )
            cursor = conn.cursor()
            print("Database connection was successful!")
            return conn, cursor

        except Exception as error:
            print("Connecting to database failed")
            print("Error: ", error)
            time.sleep(2)

conn, cursor = get_psycopg2_connection()
