
from pydantic import BaseModel, EmailStr, Field, constr, conint, field_validator
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
    phone_number: str = constr(min_length=8, max_length=10)   # UNIQUE
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


class UserUpdate(BaseModel):
    email: EmailStr
    phone_number: str = constr(min_length=8, max_length=10)
    password: str | None = None

    @classmethod
    def from_user(cls, user: User):
        return cls(
            email=user.email,
            phone_number=user.phone_number,
            password=None
        )


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
    number: constr(min_length=13, max_length=19)
    expiration_date: date | None = datetime.now()
    cardholder_name: constr(min_length=2, max_length=30)
    cvv: conint(ge=100, le=999)
    wallet_id: int | None = None
    is_virtual: bool | None = Field(default=False)

    @field_validator('number')
    def validate_card_number(cls, value):    #card_number = "4242 4242 4242 4242"

        # Remove any spaces and convert to a list of integers
        card_number = [int(digit) for digit in value.replace(" ", "")]

        # Double every second digit from right to left
        for i in range(len(card_number) - 2, -1, -2):
            card_number[i] *= 2
            if card_number[i] > 9:
                card_number[i] -= 9

            # Sum all the digits
        total_sum = sum(card_number)

        if not total_sum % 10 == 0:
            raise ValueError('The card number is not valid')
        return value

    @classmethod
    def from_query_result(cls, number: str, expiration_date: date,
                          cardholder_name: str,cvv: int, wallet_id: int, is_virtual: bool):
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
    is_recurring: bool | None = Field(default=False)
    amount: float
    status: str = Field(default=Status.PENDING, description="Transaction status, e.g., 'pending', 'confirmed', 'denied'")
    message: str | None = None
    recurring_period: int | None = None
    recurring_date: date | None = datetime.now()
    transaction_date: date = datetime.now()
    wallet_id: int | None = None
    receiver_id: int | None = None
    contact_list_id: int | None = None

    @field_validator('is_recurring')
    def validate_recurring_state(cls, value):
        if value == 1:
            return True
        return False


    @classmethod
    def from_query_result(cls, id: int, is_recurring: bool, amount: float,
                          status: str, message: str|None, transaction_date: date,
                          recurring_date: date|None, wallet_id: int|None,
                          receiver_id: int|None, contact_list_id: int = None):

        return cls(id=id,
                   is_recurring= cls.validate_recurring_state(is_recurring),
                   amount=amount,
                   status=status,
                   message=message,
                   transaction_date=transaction_date,
                   recurring_date=recurring_date,
                   wallet_id=wallet_id,
                   receiver_id=receiver_id,
                   contact_list_id=contact_list_id)

class UserTransfer(BaseModel):

    username: str | None = None
    phone_number: str = None
    amount: float = Field(gt=0.1)
     # transaction_date = date.today()

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
    id: int | None or None
    contact_name: str | constr(min_length=2, max_length=100) = None
    contact_email: EmailStr | None = None
    iban: str | constr(min_length=15, max_length=34) = None

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



