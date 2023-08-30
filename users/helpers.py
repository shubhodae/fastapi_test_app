from typing import List
from fastapi import HTTPException, status
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from test_app.settings import AppSettings
from test_app.helpers import ModelHandler
from .models import User
from .schemas import UserInDBSchema, UserSchema, UserUpdateSchema, UserIDSchema

from jose import jwt
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


class UserAuthenticator:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def __get_user_by_username_or_email(self, username_or_email: str) -> UserInDBSchema:
        query = await self.db.execute(
            select(User).filter(
                (User.username == username_or_email) | (User.email == username_or_email),
                User.is_active == True
            )
        )
        user_obj = query.scalar_one_or_none()
        if not user_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user not found"
            )
        return user_obj

    def verify_password(self, password, hashed_password) -> bool:
        return PasswordHasher.verify_password(password, hashed_password)

    async def authenticate_user(self, username_or_email: str, password: str) -> UserSchema | None:
        user = await self.__get_user_by_username_or_email(username_or_email)
        if not self.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username/email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        if False == user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User inactive",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user



class UserHandler(ModelHandler):

    def __init__(self, db: AsyncSession):
        self.db = db


    def __hash_password(self, password) -> str:
        return PasswordHasher.hash_password(password)


    async def create(self, user: UserInDBSchema) -> UserSchema:
        user.password = self.__hash_password(user.password)
        user_obj = User(**user.dict())
        self.db.add(user_obj)
        await self.db.commit()
        await self.db.refresh(user_obj)
        return user_obj


    async def get(self, user_id: int) -> UserSchema:
        query = await self.db.execute(
            select(User).filter(
                User.id == user_id,
                User.is_active == True
            )
        )
        user_obj = query.scalar_one_or_none()
        if user_obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active user not found"
            )
        return user_obj


    async def list(self) -> List[UserSchema]:
        query = await self.db.execute(
            select(User).filter(
                User.is_active == True
            )
        )
        user_list = query.scalars().all()
        return user_list


    async def update(self, user_id: int, user_data: UserUpdateSchema) -> UserInDBSchema:
        user_obj = await self.get(user_id)
        user_dict = user_data.dict(exclude_unset=True)
        for key, value in user_dict.items():
            setattr(user_obj, key, value)
        self.db.add(user_obj)
        await self.db.commit()
        await self.db.refresh(user_obj)
        return user_obj


    async def delete(self, user_id: int) -> UserInDBSchema:
        user_obj = await self.get(user_id)
        user_obj.is_active = False
        self.db.add(user_obj)
        await self.db.commit()
        await self.db.refresh(user_obj)
        return user_obj


def create_access_token(settings: AppSettings, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire
    })
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
