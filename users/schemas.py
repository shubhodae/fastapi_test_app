from pydantic import BaseModel
from datetime import datetime


class UserBaseSchema(BaseModel):
    name: str
    email: str
    username: str

class UserSchema(UserBaseSchema):
    phone: str | None = None
    is_active: bool = False

    class Config:
        orm_mode = True

class UserInDBSchema(UserSchema):
    password: str

class UserIDSchema(BaseModel):
    id: int
