from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    email: EmailStr
    username: str = Field(min_length=1, max_length=128)
    phone: str | None = Field(min_length=1, max_length=15, default=None)

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
    name: str | None = Field(min_length=1, max_length=128, default=None)
    phone: str | None = Field(min_length=1, max_length=15, default=None)


class Token(BaseModel):
    access_token: str
    token_type: str
