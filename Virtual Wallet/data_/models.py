
from pydantic import BaseModel, EmailStr, Field, constr, conint
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
    email: EmailStr                             # Valid and UNIQUE!!!!
    phone_number: str = Field(max_length=10)    # UNIQUE
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
                   hashed_password=hashed_password,
                   role=role,
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


class Card(BaseModel):

    id: int | None = None
    number: constr(min_length=16, max_length=16)   # random number from the app, cuz we create the card?   # create
    expiration_date: date #= Field(default_factory=lambda: datetime.today().date() + relativedelta(years=5))  # random date from the app, cuz we create the card?   # create
    cardholder_name: constr(min_length=2, max_length=30)   # String field with length between 2 and 30 characters
    cvv: conint(ge=100, le=999)   # random 3 numbers za create
    wallet_id: int | None = None
    is_virtual: bool = Field(default=False)

    @classmethod
    def from_query_result(cls, number: str, expiration_date: date, cardholder_name: str, cvv: int, wallet_id: int, is_virtual: bool ):
        return cls(
                   number=number,
                   expiration_date=expiration_date,
                   cardholder_name=cardholder_name,
                   cvv=cvv,
                   wallet_id=wallet_id,
                   is_virtual=is_virtual
        )


class Transactions(BaseModel):

    id: int | None = None
    is_recurring: bool = Field(default=False)
    amount: float
    status: str | None = None
    message: str | None = None
    recurring_period: int | None = None
    recurring_date: date | None = datetime.now()
    transaction_date: date = datetime.now()
    wallet_id: int | None = None
    receiver_id: int | None = None

    @classmethod
    def from_query_result(cls, id: int, is_recurring: bool, amount: float, status: str, message: str,
                          transaction_date: date, wallet_id: int, receiver_id: int, recurring_period: int = None, recurring_date: date = None):
        return cls(id=id,
                   is_recurring=is_recurring,
                   amount=amount,
                   status=status,
                   message=message,
                   transaction_date=transaction_date,
                   wallet_id=wallet_id,
                   receiver_id=receiver_id,
                   recurring_period=recurring_period or None,
                   recurring_date=recurring_date or None)


# class TransactionHistory(BaseModel):
#
#     user_id: int
#     transaction_id: int | None = None
#     recurring_date: date = datetime.now()  # !
#
#     @classmethod
#     def from_query_result(cls, user_id: int, transaction_id: int, recurring_date:date):
#         return cls(id=id,
#                    user_id=user_id,
#                    transaction_id=transaction_id,
#                    recurring_date=recurring_date)


class Wallet(BaseModel):

    id: int | None = None
    amount: float | None = None
    user_id: int


class ContactList(BaseModel):

    id: int | None = None
    user_id: int
    contact_id: int
    amount_sent: float | None = None
    amount_received: float | None = None
    utility_iban: str | None = None

    @classmethod
    def from_query_result(cls, user_id: int, contact_id: int, amount_sent: float = None, amount_received: float = None,
                          utility_iban: str = None):
        return cls(id=id,
                   user_id=user_id,
                   contact_id=contact_id,
                   amount_sent=amount_sent or None,
                   amount_received=amount_received or None,
                   utility_iban=utility_iban or None)


class Categories(BaseModel):

    id: int | None = None
    title: str
    transaction_id: int


