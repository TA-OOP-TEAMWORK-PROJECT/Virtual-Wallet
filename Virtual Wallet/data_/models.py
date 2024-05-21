from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date
import re

<<<<<<< Updated upstream
from data_.database import read_query
=======
from pydantic import BaseModel, EmailStr, Field, constr, conint, field_validator
from datetime import date, datetime
#import numpy as np 

>>>>>>> Stashed changes


class Role:

    ADMIN = 'admin'
    USER = 'user'


class STATUS:

    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    DENIED = 'denied'

class User(BaseModel):

    id: int = None or None
    username: str = Field(max_length=20)
    password: str | None = None
    first_name: str = Field(max_length=45)
    last_name: str = Field(max_length=45)
    email: EmailStr
    phone_number: str = None
    date_of_birth: date | None = None
    role: str = Field(default=Role.USER, description="User role, e.g., 'admin', 'user'")
    wallet_id: int = None or None
    hashed_password: str | None = None
    is_blocked: bool | None = None

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one capital letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[+\-*&^]+', v):
            raise ValueError('Password must contain at least one special symbol (+, -, *, &, ^, …)')
        return v
    
    @validator('email')
    def validate_email(cls, v):
        if read_query('SELECT * FROM users WHERE email = %s', (v,)):
            raise ValueError('Email must be unique')
        return v

    @validator('phone_number')
    def validate_phone_number(cls, v):
        if not v.isdigit() or len(v) != 10:
            raise ValueError('Phone number must be exactly 10 digits')
        if read_query('SELECT * FROM users WHERE phone_number = %s', (v,)):
            raise ValueError('Phone number must be unique')
        return v


@classmethod
def from_query_result(cls, id: int, username: str, first_name: str, last_name: str, email: str, phone_number: int, wallet_id: int, is_blocked,
                          date_of_birth: date, hashed_password,role):
    return cls(id=id,
                 username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                wallet_id=wallet_id,
                date_of_birth=date_of_birth,
                hashed_password=hashed_password,
                is_blocked=is_blocked,
                role=role)

def is_admin(self):
    return self.role == Role.ADMIN

class UserInDB(User):
    hashed_password: str


class LoginData(BaseModel):

    username: str = Field(max_length=20)
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one capital letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[+\-*&^]+', v):
            raise ValueError('Password must contain at least one special symbol (+, -, *, &, ^, …)')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Card(BaseModel):
    id: int = None
    number: int = None
    exp_date: date = None
    cardholder_id: int = None
    cvv: int = None

<<<<<<< Updated upstream
    @validator('number')
    def validate_number(cls, v):
        if not v:
            raise ValueError('Card number is required')
        return v
=======
    id: int | None = None
    number: constr(min_length=13, max_length=19) # type: ignore
    expiration_date: date | None = datetime.now()
    cardholder_name: constr(min_length=2, max_length=30) # type: ignore
    cvv: conint(ge=100, le=999) # type: ignore
    wallet_id: int | None = None
    is_virtual: bool | None = Field(default=False)
>>>>>>> Stashed changes

    @validator('exp_date')
    def validate_exp_date(cls, v):
        if not v:
            raise ValueError('Expiration date is required')
        if v < date.today():
            raise ValueError('Expiration date must be in the future')
        return v

    @validator('cardholder_id')
    def validate_cardholder_id(cls, v):
        if not v:
            raise ValueError('Cardholder ID is required')
        return v

    @validator('cvv')
    def validate_cvv(cls, v):
        if not v:
            raise ValueError('CVV is required')
        if len(str(v)) != 3:
            raise ValueError('CVV must be a 3-digit number')
        return v
    

class Categories(BaseModel):
    id = int or None
    title = str
    transaction_id = int or None

class Contact_list(BaseModel):
    id = int or None
    user_id = int or None
    contact_id = int or None
    sent = str
    received = str


class Transactions(BaseModel):
    id = int or None
    is_reccuring = bool or None
    ammount = float or None
    status = str 

class TransactionHistory(BaseModel):
    user_id = int or None
    transaction_id = int or None
    reccuring_date = date or None


class Wallet(BaseModel):
<<<<<<< Updated upstream
    id = int or None
    amount = float or None
=======

    id: int | None = None
    amount: float | None = None
    user_id: int

    @classmethod
    def from_query_result(cls, id:int|None, amount, user_id):
        return cls(
            id=id,
            amount=amount,
            user_id=user_id
        )


class ContactList(BaseModel):

    id: int | None = None
    user_id: int
    contact_id: int | None = None
    external_user_id: int | None = None
    @classmethod
    def from_query_result(cls, id: int, user_id: int, contact_id: int = None, external_user_id: int = None):
        return cls(id=id,
                   user_id=user_id,
                   contact_id=contact_id,
                   external_user_id=external_user_id)


class ViewContacts(BaseModel):
    id: int
    contact_name: str | None = None
    email: EmailStr
    phone_or_iban: str | None = None


class ExternalContacts(BaseModel):
    id: int | None or None # type: ignore
    contact_name: str | constr(min_length=2, max_length=100) = None # type: ignore
    contact_email: EmailStr | None = None
    iban: str | constr(min_length=15, max_length=34) = None # type: ignore

    @classmethod
    def from_query_result(cls, id: int, contact_name: str = None, contact_email: EmailStr = None, iban: str = None):
        return cls(id=id, contact_name=contact_name, contact_email=contact_email, iban=iban)


class Categories(BaseModel):

    id: int | None = None
    title: str
    transaction_id: int

    @classmethod
    def from_query_result(cls, id: int, title: str, transaction_id: int = None):
        return cls(id=id,
                   title=title,
                   transaction_id=transaction_id or None
                   )


class AccountDetails(BaseModel): #
    user: User
    cards: list[Card]
    categories: list[Categories]
    contacts: list[ContactList]
    transactions: list[Transactions]



>>>>>>> Stashed changes
