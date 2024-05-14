from common import auth
from data_.models import *
from data_.database import read_query, insert_query
from fastapi import HTTPException, Header


def create(username: str, password: str, first_name: str, last_name: str, email: str,
           date_of_birth: date) -> User | None:

    existing_user = read_query('SELECT id FROM users WHERE username = ?', (username,))
    if existing_user:
        raise HTTPException(status_code=400, detail=f'Username {username} is taken.')

    hash_password = auth.get_password_hash(password)

    generated_id = insert_query(
        'INSERT INTO users(username, first_name, last_name, email, date_of_birth, hashed_password) VALUES (?,?,?,?,?,?)',
        (username, first_name, last_name, email, date_of_birth, hash_password))


    return  User(id=generated_id, username=username, password=password, first_name=first_name, last_name=last_name,
                email=email, date_of_birth=date_of_birth, hashed_password=hash_password)

def find_by_username(username: str) -> User | None:
    data = read_query(
        '''SELECT id, username, first_name,
        last_name, email, date_of_birth, hashed_password, role
        FROM users WHERE username = ?''',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)