from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field('first_name', min_length=3, max_length=20)
    last_name: str = Field('last_name', min_length=3, max_length=20)
    email: EmailStr
    phone_number: str = Field('phone_number', min_length=5, max_length=30)
    birthday: datetime
    description: str = Field('description', min_length=10, max_length=200)


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: datetime
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
