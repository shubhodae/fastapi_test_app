from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime

from .settings import DatabaseSettings


db_settings = DatabaseSettings()
engine = create_engine(db_settings.SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_on = Column(DateTime, default=datetime.now)
    modified_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)