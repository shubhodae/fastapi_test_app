from pydantic import BaseSettings, PostgresDsn
import os


class Settings(BaseSettings):
    # APP Settings
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database settings
    pg_dsn: PostgresDsn = os.getenv("SQLALCHEMY_DATABASE_URL", default="postgresql://postgres:tiger@db/test_db")
