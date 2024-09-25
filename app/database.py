from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = "sqlite:///./users.db"
engine = create_engine(DATABASE_URI , connect_args={"check_same_thread" : False})

SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()