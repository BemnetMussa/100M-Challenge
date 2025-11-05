from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@db/eventlog"
engine = create_engine(SQLALCHEMY_DATABASE_URL) # core interface to the db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # SessionLocal class create new db sessions
Base = declarative_base() # used by models (from models.py)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
