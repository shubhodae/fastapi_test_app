from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from datetime import datetime

from .settings import DatabaseSettings


db_settings = DatabaseSettings()
engine = create_async_engine(db_settings.SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()



class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_on = Column(DateTime, default=datetime.now)
    modified_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)