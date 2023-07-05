from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str
    username: str
    phone: str | None = None
    is_active: bool = True

    class Config:
        orm_mode = True


class UserWithPasswordSchema(UserSchema):
    password: str

    class Config:
        orm_mode = True


class UserInDBSchema(UserSchema):
    id: int

    class Config:
        orm_mode = True


class UserIDSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: str | None
    phone: str | None
    is_active: bool | None


class Token(BaseModel):
    access_token: str
    token_type: str
