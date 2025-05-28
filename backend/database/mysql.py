import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import pymysql

load_dotenv()


SQL_SERVER_HOST = os.getenv("SQL_SERVER_HOST")
SQL_SERVER_DB = os.getenv("SQL_SERVER_DB")
SQL_SERVER_USER = os.getenv("SQL_SERVER_USER")
SQL_SERVER_PASSWORD = os.getenv("SQL_SERVER_PASSWORD")
SQL_SERVER_PORT = os.getenv("SQL_SERVER_PORT", "3306")

SQL_SERVER_URL = f"mysql+pymysql://{SQL_SERVER_USER}:{SQL_SERVER_PASSWORD}@{SQL_SERVER_HOST}:{SQL_SERVER_PORT}/{SQL_SERVER_DB}"

# Create a new SQLAlchemy engine instance
engine = create_engine(SQL_SERVER_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
