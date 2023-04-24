from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr

from src.database.models import Role


class ContactModel(BaseModel):
    first_name: str = Field('first_name', min_length=3, max_length=20)
    last_name: str = Field('last_name', min_length=3, max_length=20)
    email: EmailStr
    phone_number: str = Field('phone_number', min_length=5, max_length=30)
    birthday: date
    description: str = Field('description', min_length=10, max_length=200)


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


# class UserDb(BaseModel):
#     id: int
#     username: str
#     email: str
#     created_at: datetime
#     roles: Role
#     avatar: str
#
#     class Config:
#         orm_mode = True


class UserResponse(BaseModel):
    # user: UserDb
    # detail: str = "User successfully created"
    id: int
    username: str
    email: str
    created_at: datetime
    roles: Role
    avatar: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
