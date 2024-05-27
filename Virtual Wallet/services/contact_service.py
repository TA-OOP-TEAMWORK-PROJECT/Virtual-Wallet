from common import auth
from common.response import NotFound
from data_.models import *
from data_.database import read_query, insert_query, update_query
from fastapi import HTTPException
from data_.models import User
from services.admin_service import send_registration_email
from services.user_service import find_by_id, get_user_wallet, get_user_cards, get_user_categories, get_user_contacts, \
    get_user_transactions, find_by_username


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


def get_username_by(user_id: int, search: str, contact_list: bool = False, is_external=None) -> dict:
    results = []


    if not is_external:   #за да не проверява в таблицата Users без да има нужда
        user_data = read_query('''
                SELECT username 
                FROM users
                WHERE email LIKE ?
                OR username LIKE ?
                OR phone_number LIKE ?''',
                (f'%{search}%', f'%{search}%', f'%{search}%'))

        for row in user_data:
            results.append(row[0])

    if contact_list and is_external:
        external_user_data = read_query('''
                    SELECT external_user.contact_name 
                    FROM external_user
                    JOIN contact_list ON external_user.id = contact_list.external_user_id
                    WHERE contact_list.user_id = ?
                    AND (external_user.contact_name LIKE ?
                    OR external_user.contact_email LIKE ?
                    OR external_user.iban LIKE ?)''',
                    (user_id, f'%{search}%', f'%{search}%', f'%{search}%'))

        for row in external_user_data:
            results.append(row[0])

    if contact_list and not is_external:

        user_data = read_query('''
            SELECT users.username 
            FROM users
            JOIN contact_list ON users.id = contact_list.contact_id
            WHERE contact_list.user_id = ?
            AND (users.email LIKE ?
            OR users.username LIKE ?
            OR users.phone_number LIKE ?)''',
            (user_id, f'%{search}%', f'%{search}%', f'%{search}%'))

        for row in user_data:
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
        SELECT cl.id, cl.external_user_id
        FROM contact_list cl
        WHERE cl.user_id = ? AND cl.external_user_id = ?
    ''', (user_id, removed_user_id))

    contact_list = internal_contact + external_contact
    if not contact_list:
        raise HTTPException(status_code=404, detail="Contact not found in your contact list.")

    contact_id = contact_list[0][0]
    external_user_id = contact_list[0][1] if external_contact else None

    update_query('''DELETE FROM contact_list WHERE id = ?''', (contact_id,))

    if external_user_id:
        update_query('''DELETE FROM external_user WHERE id = ?''', (external_user_id,))

    return True


def get_contact_list(current_user, contact_name):

    data = read_query('''
    SELECT contact_list.id, user_id, external_user_id
    FROM contact_list
    JOIN external_user
    ON external_user.id = contact_list.external_user_id
    WHERE contact_list.user_id = ?
    AND external_user.contact_name = ?''',
    (current_user.id, contact_name))

    id, user_id, external_user_id = data[0]
    return ContactList(id=id, user_id=user_id, external_user_id=external_user_id)
