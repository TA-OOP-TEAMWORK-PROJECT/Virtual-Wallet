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



    return  User(id=generated_id, username=username, password=password, first_name=first_name, last_name=last_name,
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


def update_user_profile(username: str, user_update: UserUpdate) -> User | None:
    hashed_password = auth.get_password_hash(user_update.password) if user_update.password else None
    update_query(
        '''UPDATE users SET email = ?, phone_number = ?, hashed_password = ? WHERE username = ?''',
        (user_update.email, user_update.phone_number, hashed_password, username)
    )
    return find_by_username(username)
