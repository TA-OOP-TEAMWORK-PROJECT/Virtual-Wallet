from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date
import re

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

    @validator('number')
    def validate_number(cls, v):
        if not v:
            raise ValueError('Card number is required')
        return v

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
    id = int or None
    amount = float or None