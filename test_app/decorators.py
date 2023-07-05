from functools import wraps

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError


def exception_handler_decorator(logger=None):
    def actual_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HTTPException as e:
                raise e
            except IntegrityError as e:
                logger.exception(e)
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"ERROR: Conflict, data already exists"
                )
            except Exception as e:
                if logger:
                    logger.exception(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="ERROR: Internal Server Error"
                )
        return wrapper
    return actual_decorator
