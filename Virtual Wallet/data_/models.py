
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
import numpy as np


class Role:

    ADMIN = 'admin'
    USER = 'user'


class Status:

    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    DENIED = 'denied'


class User(BaseModel):

    id: int | None = None
    username: str = Field(min_length=2, max_length=20)
    password: str | None = None
    first_name: str = Field(max_length=45)
    last_name: str = Field(max_length=45)
    email: EmailStr
    phone_number: str = Field(max_length=10)
    role: str = Field(default=Role.USER, description="User role, e.g., 'admin', 'user'")
    hashed_password: str | None = None
    is_blocked: bool = Field(default=False)
    disabled: bool | None = None

    @classmethod
    def from_query_result(cls, id: int, username: str, first_name: str, last_name: str, email: str,
                          phone_number: str, role, hashed_password, is_blocked):
        return cls(id=id,
                   username=username,
                   first_name=first_name,
                   last_name=last_name,
                   email=email,
                   phone_number=phone_number,
                   role=role,
                   hashed_password=hashed_password,
                   is_blocked=is_blocked)

    def is_admin(self):
        return self.role == Role.ADMIN


class UserInDB(User):
    hashed_password: str


class LoginData(BaseModel):

    username: str = Field(min_length=2, max_length=20)
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Cards(BaseModel):

    id: int | None = None
    number: str = Field(length=16)
    expiration_date: date = np.datetime64('2022') + np.timedelta64(5,'Y')   ####TODO
    cardholder_id: int
    cvv: int = Field(length=3)

    @classmethod
    def from_query_result(cls, id: int, number: str, expiration_date: date, cardholder_id: int, cvv: int):
        return cls(id=id,
                   number=number,
                   expiration_date=expiration_date,
                   cardholder_id=cardholder_id,
                   cvv=cvv)


class Transactions(BaseModel):

    id: int | None = None
    is_recurring: bool = Field(default=False)
    amount: float
    status: str | None = None
    message: str | None = None

    @classmethod
    def from_query_result(cls, id: int, is_recurring: bool, amount:float, status: str, message: str):
        return cls(id=id,
                   is_recurring=is_recurring,
                   amount=amount,
                   status=status,
                   message=message)


class Wallet(BaseModel):

    id: int|None = None
    amount: float|None
    user_id: int


class TransactionHistory(BaseModel):

    user_id: int
    transaction_id: int | None = None
    recurring_date: date = datetime.now()  # !

    @classmethod
    def from_query_result(cls, user_id: int, transaction_id: int, recurring_date: date):
        return cls(id=id,
                   user_id=user_id,
                   transaction_id=transaction_id,
                   recurring_date=recurring_date)


class ContactList(BaseModel):

    id: int|None = None
    user_id: int
    contact_id: int
    amount_sent: float
    amount_received: float

    @classmethod
    def from_query_result(cls, user_id: int, contact_id: int, amount_sent: date, amount_received: float):
        return cls(id=id,
                   user_id=user_id,
                   contact_id=contact_id,
                   amount_sent=amount_sent,
                   amount_received=amount_received)

class Categories(BaseModel):

    id: int|None = None
    title: str
    transaction_id: int
