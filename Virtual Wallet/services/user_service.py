from common import auth
from common.response import NotFound
from data_.models import *
from data_.database import read_query, insert_query, update_query
from fastapi import HTTPException
from data_.models import User
from services.admin_service import send_registration_email



def create(username: str, password: str, first_name: str,
           last_name: str, email: str, phone_number: str) -> User | None: ##Updated
    password_check(password)
    check_if_unique(username, email, phone_number)
    hash_password = auth.get_password_hash(password)

    generated_id = insert_query(
        '''INSERT INTO users(username, first_name, last_name, 
                email, phone_number, hashed_password) VALUES (?,?,?,?,?,?)''',
        (username, first_name, last_name, email, phone_number, hash_password))

    insert_query(
        '''INSERT INTO wallet (user_id, amount) VALUES (?, ?)''',
        (generated_id, 0.0)
    )

    new_user = User(id=generated_id, username=username, password=password, first_name=first_name, last_name=last_name,
                email=email, phone_number=phone_number, hashed_password=hash_password)
    send_registration_email(new_user.email)
    return new_user


def find_by_username(username: str) -> User | None:
    data = read_query(
        '''SELECT id, username, first_name, last_name,
            email, phone_number, role, hashed_password, is_blocked
            FROM users WHERE username = ?''',
            (username, ))

    return next((User.from_query_result(*row) for row in data), None)


def find_by_phone_number(phone_number: str) :
    data = read_query(
        '''SELECT id, username, first_name, last_name,
            email, phone_number, role, hashed_password, is_blocked
            FROM users WHERE phone_number = ?''',
            (phone_number, ))

    return next((User.from_query_result(*row) for row in data), None)



def find_by_id(user_id: int) -> User: #
    data = read_query(
        '''SELECT id, username, first_name, last_name,
                  email, phone_number, role, hashed_password, is_blocked
                  FROM users WHERE id = ?''',
        (user_id,)
    )
    return next((User.from_query_result(*row) for row in data), None)


def get_user_response(user):

    return {
        'Username': user.username,
        'Name': f'{user.first_name} {user.last_name}',
        'Email': user.email,
        'Phone Number': user.phone_number
    }


def update_user_profile(username: str, user_update: UserUpdate):
    current_user = find_by_username(username)
    if not current_user:
        return None

    if user_update.email != current_user.email or user_update.phone_number != current_user.phone_number:
        check_if_unique(
            email=user_update.email if user_update.email != current_user.email else current_user.email,
            phone_number=user_update.phone_number if user_update.phone_number != current_user.phone_number else current_user.phone_number
        )

    update_fields = []
    update_params = []
    message_parts = []

    if user_update.email != current_user.email:
        update_fields.append("email = ?")
        update_params.append(user_update.email)
        message_parts.append(f"email from {current_user.email} to {user_update.email}")

    if user_update.phone_number != current_user.phone_number:
        update_fields.append("phone_number = ?")
        update_params.append(user_update.phone_number)
        message_parts.append(f"phone number from {current_user.phone_number} to {user_update.phone_number}")

    if user_update.password:
        password_check(user_update.password)
        hashed_password = auth.get_password_hash(user_update.password)
        update_fields.append("hashed_password = ?")
        update_params.append(hashed_password)
        message_parts.append("password")

    if not update_fields:
        return "No changes detected."

    update_params.append(username)
    update_query(f'''UPDATE users SET {", ".join(update_fields)} WHERE username = ?''', tuple(update_params))

    message = f"User '{username}' successfully updated their: " + ", ".join(message_parts) + "."
    return message


def get_user_account_details(user_id: int) -> AccountDetails:  #  Дали можем да направим търсене само веднъж, да създадем клас и така да върнем инфото
    user = find_by_id(user_id)
    wallet = get_user_wallet(user_id)
    wallet_id = wallet.id
    cards = get_user_cards(wallet_id)
    categories = get_user_categories(user_id)
    contacts = get_user_contacts(user_id)
    transactions = get_user_transactions(wallet_id)

    return AccountDetails(
        user=user,
        cards=cards,
        categories=categories,
        contacts=contacts,
        transactions=transactions
    )





def get_user_cards(wallet_id: int) -> list[Card]:
    data = read_query(
        '''SELECT id, number, exp_date, cardholder_name, cvv, wallet_id, is_virtual
                  FROM cards WHERE wallet_id = ?''',
        (wallet_id,)
    )

    return [Card.from_query_result(*row) for row in data]


def get_user_wallet(user_id: int):

    data = read_query('''
    SELECT id, amount, user_id
    FROM wallet
    WHERE user_id = ?''',
    (user_id, ))

    return [Wallet.from_query_result(*row) for row in data][0]  #!!!


def get_user_categories(user_id: int) -> list[Categories]:
    data = read_query(
        '''SELECT id, title, user_id FROM categories WHERE user_id = ?''',
        (user_id,)
    )
    return [Categories.from_query_result(*row) for row in data]


def get_user_contacts(user_id: int) -> list[ContactList]:
    data = read_query(
        '''SELECT id, user_id, contact_id, external_user_id FROM contact_list WHERE user_id = ?''',
        (user_id,)
    )
    return [ContactList.from_query_result(*row) for row in data]

def get_contact_external_user(contact_list_id:int):
    data = read_query(
        '''SELECT e.id, e.contact_name, e.contact_email, e.iban
                FROM external_user e
                JOIN contact_list c 
                WHERE c.id = 16
                AND e.id = c.external_user_id''',
        (contact_list_id, ))

    return [ExternalContacts.from_query_result(*row) for row in data][0]

def get_user_transactions(wallet_id: int) -> list[Transactions]:  # тук излизат само тези, които са изпратени от юзъра TODO
    data = read_query(
        '''SELECT id, is_recurring, amount, status, message, recurring_period, 
                  recurring_date, transaction_date, wallet_id, receiver_id, category_id
           FROM transactions WHERE wallet_id = ?''',
        (wallet_id,)
    )
    return [Transactions.from_query_result(*row) for row in data]


def check_if_unique(username: str = None, email: str = None, phone_number: str = None):
    if username:
        existing_user = read_query('SELECT id FROM users WHERE username = ?', (username,))
        if existing_user:
            raise HTTPException(status_code=400, detail=f'Username {username} is taken.')
    if email:
        existing_email = read_query('SELECT id FROM users WHERE email = ?', (email,))
        if existing_email:
            raise HTTPException(status_code=400, detail=f'Email {email} is taken.')
    if phone_number:
        existing_phone_number = read_query('SELECT id FROM users WHERE phone_number = ?', (phone_number,))
        if existing_phone_number:
            raise HTTPException(status_code=400, detail=f'Phone number {phone_number} is taken.')


def password_check(password: str) -> str:
    if not any(char.isdigit() for char in password):
        raise HTTPException(status_code=400, detail='Password must contain at least one digit')
    if not any(char.isupper() for char in password):
        raise HTTPException(status_code=400, detail='Password must contain at least one uppercase letter')
    if not any(char.islower() for char in password):
        raise HTTPException(status_code=400, detail='Password must contain at least one lowercase letter')
    if not any(char in '+-*^&' for char in password):
        raise HTTPException(status_code=400, detail='Password must contain at least one special character (+, -, *, ^, &)')
    return password


