from pydantic import BaseSettings, PostgresDsn


class AppSettings(BaseSettings):
    ENVIRONMENT: str = 'local'
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class DatabaseSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: PostgresDsn = "postgresql://postgres:tiger@db/test_db"