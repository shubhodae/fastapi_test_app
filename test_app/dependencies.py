
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated

from jose import jwt

from .settings import SECRET_KEY, ALGORITHM

import logging
logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> int:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # logger.debug(f"Token payload: {payload}")
    user_id = payload.get("id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user_id
