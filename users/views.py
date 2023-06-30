from fastapi import APIRouter, Body, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

from test_app.database import get_db
from test_app.decorators import exception_handler_decorator

from .models import User
from .schemas import UserBaseSchema, UserSchema, UserIDSchema, UserInDBSchema
from .helpers import UserHandler

import logging
logger = logging.getLogger(__name__)



router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=UserIDSchema)
@exception_handler_decorator(logger)
def sign_up(
    user_data: Annotated[UserInDBSchema, Body(embed=True)],
    db: Session = Depends(get_db)
):
    handler_obj = UserHandler(db=db)
    user = handler_obj.create_user(user_data)
    logger.info(f"user created: {user.email}")
    return UserIDSchema(id=user.id)


@router.get("/")
async def get_user_list():
    return {
        "hello": "world"
    }
