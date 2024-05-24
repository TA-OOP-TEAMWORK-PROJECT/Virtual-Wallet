from common import auth
from common.response import NotFound
from data_.models import *
from data_.database import read_query, insert_query, update_query
from fastapi import HTTPException
from data_.models import User
from services.admin_service import send_registration_email

def create(username: str, password: str, first_name: str,
           last_name: str, email: str, phone_number: str) -> User | None: ##Updated

    existing_user = read_query('SELECT id FROM users WHERE username = ?', (username,))
    if existing_user:
        raise HTTPException(status_code=400, detail=f'Username {username} is taken.')

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


def get_user_account_details(user_id: int) -> AccountDetails:  #  Дали можем да направим търсене само веднъж, да създадем клас и така да върнем инфото
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


def find_by_id(user_id: int) -> User: #
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


def get_user_wallet(user_id: int):

    data = read_query('''
    SELECT id, amount, user_id
    FROM wallet
    WHERE user_id = ?''',
    (user_id, ))

    return [Wallet.from_query_result(*row) for row in data][0]  #!!!


def get_user_categories(transaction_id: int) -> list[Categories]:
    data = read_query(
        '''SELECT id, title FROM categories WHERE transaction_id = ?''',
        (transaction_id,)
    )
    return [Categories.from_query_result(*row) for row in data]


def get_user_contacts(user_id: int) -> list[ContactList]:
    data = read_query(
        '''SELECT id, user_id, contact_id, external_user_id FROM contact_list WHERE user_id = ?''',
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


def get_username_by(user_id: int, search: str, contact_list: bool = False) -> dict:
    results = []

    user_data = read_query('''
        SELECT username 
        FROM users
        WHERE email LIKE ?
        OR username LIKE ?
        OR phone_number LIKE ?''',
        (f'%{search}%', f'%{search}%', f'%{search}%'))

    for row in user_data:
        results.append(row[0])

    if contact_list:
        user_data = read_query('''
            SELECT users.username 
            FROM users
            JOIN contact_list ON users.id = contact_list.contact_id
            WHERE contact_list.user_id = ?
            AND (users.email LIKE ?
            OR users.username LIKE ?
            OR users.phone_number LIKE ?)''',
            (user_id, f'%{search}%', f'%{search}%', f'%{search}%'))

        external_user_data = read_query('''
            SELECT external_user.contact_name 
            FROM external_user
            JOIN contact_list ON external_user.id = contact_list.external_user_id
            WHERE contact_list.user_id = ?
            AND (external_user.contact_name LIKE ?
            OR external_user.contact_email LIKE ?
            OR external_user.iban LIKE ?)''',
            (user_id, f'%{search}%', f'%{search}%', f'%{search}%'))

        for row in user_data:
            results.append(row[0])

        for row in external_user_data:
            results.append(row[0])

    if not results:
        raise HTTPException(status_code=404, detail="No such user in the system, maybe check your contact list?")

    result_dict = {i + 1: result for i, result in enumerate(results)}

    return result_dict  # ako nqma zapisi? # Оправено

def view_user_contacts(user_id: int) -> list[ViewContacts]: #Easter Egg
    data = read_query(
        '''SELECT contact_list.id,  
                  CASE 
                      WHEN contact_list.contact_id IS NOT NULL THEN users.username 
                      ELSE external_user.contact_name 
                  END AS contact_name,
                  CASE 
                      WHEN contact_list.contact_id IS NOT NULL THEN users.email 
                      ELSE external_user.contact_email 
                  END AS email,
                  CASE 
                      WHEN contact_list.contact_id IS NOT NULL THEN users.phone_number 
                      ELSE external_user.iban 
                  END AS phone_or_iban
           FROM contact_list 
           LEFT JOIN users ON contact_list.contact_id = users.id 
           LEFT JOIN external_user ON contact_list.external_user_id = external_user.id
           WHERE contact_list.user_id = ?''',
        (user_id,)
    )
    return [ViewContacts(id=row[0], contact_name=row[1], email=row[2], phone_or_iban=row[3]) for row in data]


def add_user_to_contacts(user_id: int, contact_username: str) -> ContactList:
    contact_user = find_by_username(contact_username)
    if not contact_user:
        raise HTTPException(status_code=404, detail="No such user")

    existing_contact = read_query(
        '''SELECT id FROM contact_list WHERE user_id = ? AND contact_id = ?''',
        (user_id, contact_user.id)
    )
    if existing_contact:
        raise HTTPException(status_code=400, detail="Contact already exists")

    contact_id = insert_query(
        '''INSERT INTO contact_list (user_id, contact_id) VALUES (?, ?)''',
        (user_id, contact_user.id)
    )
    return ContactList(id=contact_id, user_id=user_id, contact_id=contact_user.id)



def add_external_contact(user_id: int, contact_data: ExternalContacts) -> ContactList:
    existing_external_user = read_query(
        '''SELECT id FROM contact_list WHERE user_id = ? AND external_user_id = ?''',
        (user_id, contact_data.iban))

    if existing_external_user:
        external_user_id = existing_external_user[0][0]
    else:
        external_user_id = insert_query(
            '''INSERT INTO external_user (contact_name, contact_email, iban) VALUES (?, ?, ?)''',
            (contact_data.contact_name, contact_data.contact_email, contact_data.iban))

    existing_contact = read_query(
        '''SELECT id FROM contact_list WHERE user_id = ? AND external_user_id = ?''',
        (user_id, external_user_id))

    if existing_contact:
        raise HTTPException(status_code=400, detail="External contact already exists")

    contact_id = insert_query(
        '''INSERT INTO contact_list (user_id, external_user_id) VALUES (?, ?)''',
        (user_id, external_user_id))

    return ContactList(id=contact_id, user_id=user_id, external_user_id=external_user_id)


def remove_contact(user_id: int, removed_user_id: int) -> bool:
    internal_contact = read_query('''
        SELECT cl.id
        FROM contact_list cl
        WHERE cl.user_id = ? AND cl.contact_id = ?
    ''', (user_id, removed_user_id))

    external_contact = read_query('''
        SELECT cl.id
        FROM contact_list cl
        WHERE cl.user_id = ? AND cl.external_user_id = ?
    ''', (user_id, removed_user_id))

    contact_list = internal_contact + external_contact
    if not contact_list:
        raise HTTPException(status_code=404, detail="Contact not found in your contact list.")

    update_query('''DELETE FROM contact_list WHERE id = ?''', (contact_list[0][0],))

    return True

