from typing import Optional, List
from fastapi import Query
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime

from data_.database import read_query


class Role:

    ADMIN = 'admin'
    USER = 'user'


class STATUS:

    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    DENIED = 'denied'

class User(BaseModel):

    id: int = None or None
    username: str = Field(max_length=45)
    password: str | None = None
    first_name: str = Field(max_length=45)
    last_name: str = Field(max_length=45)
    email: EmailStr
    date_of_birth: date | None = None
    role: str = Field(default=Role.USER, description="User role, e.g., 'admin', 'user'")
    hashed_password: str | None = None
    disabled: bool | None = None


    @classmethod
    def from_query_result(cls, id: int, username: str, first_name: str, last_name: str, email: str,
                          date_of_birth: date, hashed_password,role):
        return cls(id=id,
                   username=username,
                   first_name=first_name,
                   last_name=last_name,
                   email=email,
                   date_of_birth=date_of_birth,
                   hashed_password=hashed_password,
                   role=role)

    def is_admin(self):
        return self.role == Role.ADMIN

class UserInDB(User):
    hashed_password: str


class LoginData(BaseModel):

    username: str = Field(max_length=45)
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
