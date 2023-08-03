from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from test_app.settings import AppSettings
from test_app.database import get_db
# from test_app.decorators import exception_handler_decorator
from test_app.dependencies import get_current_user_id, get_settings

from .schemas import UserSchema, UserIDSchema,\
    Token, UserUpdateSchema, UserWithPasswordSchema
from .helpers import UserHandler, create_access_token

from datetime import timedelta

import logging
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/signup", response_model=UserIDSchema)
# @exception_handler_decorator(logger)
def signup(
    user_data: Annotated[UserWithPasswordSchema, Body()],
    db: Session = Depends(get_db)
):
    handler_obj = UserHandler(db=db)
    try:
        user = handler_obj.create_user(user_data)
    except IntegrityError as e:
        logger.exception(f"IntegrityError: Error in user creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"ERROR: Conflict: data already exists"
        )
    except Exception as e:
        logger.exception(f"Error in user creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create user"
        )
    logger.info(f"user created: {user.email}")
    return UserIDSchema(id=user.id)


@router.post("/login", response_model=Token)
# @exception_handler_decorator(logger)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[AppSettings, Depends(get_settings)]
):
    handler_obj = UserHandler(db=db)
    try:
        user = handler_obj.authenticate_user(
            username_or_email=form_data.username,
            password=form_data.password
        )
    except Exception as e:
        logger.exception(f"Uable to authenticate user: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    access_token_expires = timedelta(minutes=30)
    try:
        access_token = create_access_token(
            settings=settings,
            data={
                "sub": user.username,
                "id": user.id
            },
            expires_delta=access_token_expires
        )
    except Exception as e:
        logger.exception(f"Unable to create access_token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create access_token"
        )
    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@router.get("/", response_model=UserSchema)
async def get_user(
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)]
):
    handler_obj = UserHandler(db=db)
    user = handler_obj.get_user(user_id)
    return user


@router.put("/", response_model=UserIDSchema)
async def update_user(
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    user_data: Annotated[UserUpdateSchema, Body(embed=True, title="user data to be updated")]
):
    handler_obj = UserHandler(db=db)
    user = handler_obj.update_user(user_id, user_data)
    return user


@router.delete("/", response_model=UserIDSchema)
async def delete_user(
    db: Annotated[Session, Depends(get_db)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    handler_obj = UserHandler(db=db)
    user = handler_obj.delete_user(user_id=user_id)
    return user
