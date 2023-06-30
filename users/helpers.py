from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .models import User
from .schemas import UserInDBSchema, UserSchema


class PasswordHasher:

    @staticmethod
    def __getcontext() -> CryptContext:
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash_password(password) -> str:
        context = PasswordHasher.__getcontext()
        return context.hash(password)

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        context = PasswordHasher.__getcontext()
        return context.verify(plain_password, hashed_password)



class UserHandler:

    def __init__(self, db: Session):
        self.db = db

    def __hasd_password(self, password) -> str:
        return PasswordHasher.hash_password(password)

    def create_user(self, user: UserInDBSchema) -> UserSchema:
        user.password = self.__hasd_password(user.password)
        user_obj = User(**user.dict())
        self.db.add(user_obj)
        self.db.commit()
        self.db.refresh(user_obj)
        return user_obj
