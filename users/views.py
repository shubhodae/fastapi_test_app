from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

from test_app.database import get_db
from test_app.decorators import exception_handler_decorator
from test_app.dependencies import get_current_user_id

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
@exception_handler_decorator(logger)
def signup(
    user_data: Annotated[UserWithPasswordSchema, Body()],
    db: Session = Depends(get_db)
):
    handler_obj = UserHandler(db=db)
    user = handler_obj.create_user(user_data)
    logger.info(f"user created: {user.email}")
    return UserIDSchema(id=user.id)


@router.post("/login", response_model=Token)
@exception_handler_decorator(logger)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    handler_obj = UserHandler(db=db)
    user = handler_obj.authenticate_user(
        username=form_data.username,
        password=form_data.password
    )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "id": user.id
        },
        expires_delta=access_token_expires
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
