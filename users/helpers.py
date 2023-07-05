from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from test_app.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .models import User
from .schemas import UserInDBSchema, UserSchema, UserUpdateSchema

from jose import jwt, JWTError
from datetime import datetime, timedelta

import logging
logger = logging.getLogger(__name__)





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

    def __hash_password(self, password) -> str:
        return PasswordHasher.hash_password(password)
    

    def __get_user_by_username_or_email(self, username: str) -> UserInDBSchema:
        user_obj = self.db.query(User).filter(
            User.username == username,
        ).first()
        if not user_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found"
            )
        return user_obj


    def verify_password(self, password, hashed_password) -> bool:
        return PasswordHasher.verify_password(password, hashed_password)


    def create_user(self, user: UserInDBSchema) -> UserSchema:
        user.password = self.__hash_password(user.password)
        user_obj = User(**user.dict())
        self.db.add(user_obj)
        self.db.commit()
        self.db.refresh(user_obj)
        return user_obj


    def authenticate_user(self, username: str, password: str) -> UserSchema | None:
        user = self.__get_user_by_username_or_email(username)
        if not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        if False == user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User inactive",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user
    

    def get_user(self, user_id: int) -> UserSchema:
        user_obj = self.db.query(User).filter(
            User.id == user_id,
            User.is_active == True
        ).first()
        if user_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active user not found"
            )
        return user_obj
    

    def update_user(self, user_id: int, user_data: UserUpdateSchema) -> UserInDBSchema:
        user_obj = self.get_user(user_id)
        user_dict = user_data.dict()
        for key, value in user_dict.items():
            setattr(user_obj, key, value)
        self.db.add(user_obj)
        self.db.commit()
        self.db.refresh(user_obj)
        return user_obj
    

    def delete_user(self, user_id: int) -> UserInDBSchema:
        user_obj = self.get_user(user_id)
        user_obj.is_active = False
        self.db.add(user_obj)
        self.db.commit()
        self.db.refresh(user_obj)
        return user_obj


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({
        "exp": expire
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
