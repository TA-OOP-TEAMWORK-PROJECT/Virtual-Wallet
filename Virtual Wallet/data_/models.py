from pydantic import BaseModel, EmailStr, Field, constr, conint, field_validator
from datetime import date, datetime


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
    first_name: str = Field(min_length=1, max_length=45)
    last_name: str = Field(min_length=1, max_length=45)
    email: EmailStr                             # Valid and UNIQUE!!!!
    phone_number: str = Field(min_length=8, max_length=10, pattern=r'^\d{8,10}$')   # UNIQUE
    role: str = Field(default=Role.USER, description="User role, e.g., 'admin', 'user'")
    hashed_password: str | None = None
    is_blocked: bool = Field(default=True)
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


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    first_name: str = Field(min_length=1, max_length=45)
    last_name: str = Field(min_length=1, max_length=45)
    email: EmailStr
    phone_number: str = Field(min_length=8, max_length=10, pattern=r'^\d{8,10}$')


class UserUpdate(BaseModel):
    email: EmailStr
    phone_number: str = Field(min_length=8, max_length=10, pattern=r'^\d{8,10}$')
    password: str = Field(min_length=8, max_length=20) or None

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
    expiration_date: date | None = None     #datetime.now()
    cardholder_name: constr(min_length=2, max_length=30) | None = None
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
    def from_query_result(cls, id: int | None, number: str, expiration_date: date, cardholder_name: str | None,
                        cvv: int, wallet_id: int | None, is_virtual: bool):
        return cls(id=id,
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
    recurring_date: date | None = None
    transaction_date: date | None = None #bez None
    wallet_id: int | None = None
    receiver_id: int | None = None
    contact_list_id: int | None = None
    category_id: int | None = None

    @field_validator('is_recurring')
    def validate_recurring_state(cls, value):
        if value == 1:
            return True
        return False

    @classmethod
    def from_query_result(cls, id: int, is_recurring: bool, amount: float,
                          status: str, message: str | None, recurring_period: int | None,
                          recurring_date: date | None, transaction_date: date,
                          wallet_id: int | None, receiver_id: int | None, contact_list_id: int | None,
                          category_id: int | None = None):
        return cls(
            id=id,
            is_recurring=cls.validate_recurring_state(is_recurring),
            amount=amount,
            status=status,
            message=message,
            recurring_period=recurring_period,
            recurring_date=recurring_date,
            transaction_date=transaction_date,
            wallet_id=wallet_id,
            receiver_id=receiver_id,
            contact_list_id=contact_list_id,
            category_id=category_id
        )

    @classmethod
    def get_transactions_query(cls, id, is_recurring, status, amount,
                               transaction_date, receiver_id, contact_list_id, recurring_date=None):

        return cls(
            id=id,
            is_recurring=is_recurring,
            status=status,
            amount=amount,
            transaction_date=transaction_date,
            receiver_id=receiver_id,
            contact_list_id=contact_list_id,
            recurring_date=recurring_date
        )



class RecurringTransaction(Transactions):

    # id: int | None = None
    # amount: float
    # recurring_period: int | None = None
    # recurring_date: date | None = datetime.now()
    # transaction_date: date = datetime.now()
    # wallet_id: int | None = None
    # contact_list_id: int

    @classmethod
    def from_query_result(cls, id: int, amount: float, recurring_period: int,
                          recurring_date: date|None, transaction_date: date, wallet_id: int|None, contact_list_id:int):

        return cls(id=id,
                   amount=amount,
                   recurring_period=recurring_period,
                   recurring_date=recurring_date,
                   transaction_date=transaction_date,
                   wallet_id=wallet_id,
                   contact_list_id=contact_list_id)


class UserTransfer(BaseModel):

    username: str | None = None
    phone_number: str|None = None
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
    def from_query_result(cls, id:int | None, amount: int | None, user_id):
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


class TransferConfirmation(BaseModel):

    new_wallet_amount: float
    receiver_wallet_amount: float
    transaction_amount: float
    transaction_date: date
    wallet_id: int
    receiver_wallet_id: int|None = None
    receiver_wallet_amount: float|None = None
    user_id: int|None = None
    receiver_id: int                   # contact_list_id if is_external is TRue else receiver_id(user in the map)
    is_external:bool


class ConfirmationResponse(BaseModel):

    is_confirmed: bool


class ExternalContacts(BaseModel):
    id: int | None = None
    contact_name: str = Field(min_length=2, max_length=100) or None
    contact_email: EmailStr | None = None
    iban: str = Field(min_length=15, max_length=34) or None

    @classmethod
    def from_query_result(cls, id: int, contact_name: str = None, contact_email: EmailStr = None, iban: str = None):
        return cls(id=id, contact_name=contact_name, contact_email=contact_email, iban=iban)


class ExternalTransfer(ExternalContacts, BaseModel):
    is_recurring: int|None = None
    recurring_date: date|None = None
    recurring_period: int|None = None
    iban: str | constr(min_length=15, max_length=34)

    @classmethod
    def from_query_result(cls, id: int, contact_name: str = None, contact_email: EmailStr = None, iban: str = None):
        return cls(id=id, contact_name=contact_name, contact_email=contact_email, iban=iban)


class Categories(BaseModel):

    id: int | None = None
    title: str
    user_id: int

    @classmethod
    def from_query_result(cls, id: int = None, title: str = None, user_id: int = None):
        return cls(id=id,
                   title=title,
                   user_id=user_id
                   )


class AccountDetails(BaseModel): #
    user: User
    cards: list[Card]
    categories: list[Categories]
    contacts: list[ContactList]
    transactions: list[Transactions]