from common import auth
from data_.models import *
from data_.database import read_query, insert_query, update_query
from fastapi import HTTPException
from data_.models import User


def create(username: str, password: str, first_name: str,
           last_name: str, email: str, phone_number: str) -> User | None:

    existing_user = read_query('SELECT id FROM users WHERE username = ?', (username,))
    if existing_user:
        raise HTTPException(status_code=400, detail=f'Username {username} is taken.')

    hash_password = auth.get_password_hash(password)

    generated_id = insert_query(
        '''INSERT INTO users(username, first_name, last_name, 
                email, phone_number, hashed_password) VALUES (?,?,?,?,?,?)''',
        (username, first_name, last_name, email, phone_number, hash_password))

    return User(id=generated_id, username=username, password=password, first_name=first_name, last_name=last_name,
                email=email, phone_number=phone_number, hashed_password=hash_password)


def find_by_username(username: str) -> User | None:
    data = read_query(
        '''SELECT id, username, first_name, last_name,
            email, phone_number, role, hashed_password, is_blocked
            FROM users WHERE username = ?''',
            (username, ))

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


def get_user_account_details(user_id: int) -> AccountDetails:
    user = find_by_id(user_id)
    cards = get_user_cards(user_id)
    categories = get_user_categories(user_id)
    contacts = get_user_contacts(user_id)
    transactions = get_user_transactions(user_id)

    return AccountDetails(
        user=user,
        cards=cards,
        categories=categories,
        contacts=contacts,
        transactions=transactions
    )


def find_by_id(user_id: int) -> User:
    data = read_query(
        '''SELECT id, username, first_name, last_name,
                  email, phone_number, role, hashed_password, is_blocked
                  FROM users WHERE id = ?''',
        (user_id,)
    )
    return next((User.from_query_result(*row) for row in data), None)


def get_user_cards(wallet_id: int) -> list[Card]:
    data = read_query(
        '''SELECT id, number, exp_date, cardholder_name, cvv, is_virtual
                  FROM cards WHERE wallet_id = ?''',
        (wallet_id,)
    )

    return [Card.from_query_result(*row) for row in data]


def get_user_categories(transaction_id: int) -> list[Categories]:
    data = read_query(
        '''SELECT id, title FROM categories WHERE transaction_id = ?''',
        (transaction_id,)
    )
    return [Categories.from_query_result(*row) for row in data]


def get_user_contacts(user_id: int) -> list[ContactList]:
    data = read_query(
        '''SELECT id, user_id, contact_id, amount_sent, amount_received, utility_iban FROM contact_list WHERE user_id = ?''',
        (user_id,)
    )
    return [ContactList.from_query_result(*row) for row in data]


def get_user_transactions(wallet_id: int) -> list[Transactions]:
    data = read_query(
        '''SELECT id, is_recurring, amount, status, message, recurring_period, recurring_date, transaction_date, receiver_id
                  FROM transactions WHERE wallet_id = ?''',
        (wallet_id,)
    )
    return [Transactions.from_query_result(*row) for row in data]


