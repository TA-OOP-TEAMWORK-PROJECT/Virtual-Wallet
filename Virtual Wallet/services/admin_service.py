from datetime import date, datetime
from typing import List, Optional
from data_.models import Transactions, User
import requests
from data_.database import update_query, read_query
from data_.database import _get_connection
from common.config import MAILJET_API_KEY, MAILJET_API_SECRET, ADMIN_EMAIL

def block_user(user_id: int):

    user_result = read_query("SELECT id FROM users WHERE id = ?", (user_id,))
    if not user_result:
        raise ValueError(f'No user found with id {user_id}')

    update_query("UPDATE users SET is_blocked = 1 WHERE id = ?", (user_id,))
    
    return 'User blocked successfully'


def unblock_user(user_id: int):

    user_result = read_query("SELECT id FROM users WHERE id = ?", (user_id,))
    if not user_result:
        raise ValueError(f'No user found with id {user_id}')

    

    update_query("UPDATE users SET is_blocked = 0 WHERE id = ?", (user_id,))

    return 'User unblocked successfully!'


def send_registration_email(email):
    url = 'https://api.mailjet.com/v3.1/send'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'Messages': [
            {
                'From': {
                    'Email': ADMIN_EMAIL,
                    'Name': 'Your Name'
                },
                'To': [
                    {
                        'Email': ADMIN_EMAIL,
                        'Name': 'Admin'
                    }
                ],
                'Subject': 'New User Registration',
                'TextPart': f'A new user has registered: {email}. Please review and approve the registration.',
                'HTMLPart': f'<h3>A new user has registered: {email}</h3><p>Please review and approve the registration.</p>'
            }
        ]
    }
    response = requests.post(url, auth=(MAILJET_API_KEY, MAILJET_API_SECRET), json=data)
    return response.status_code == 200

def approve_user(user_id):
    connection = _get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE users SET is_blocked = 0 WHERE id = ?",
        (user_id,)
    )
    connection.commit()
    connection.close()

def get_all_transactions(page: int = 1,
                         page_size: int = 10,
                         period_start: Optional[date] = None,
                         period_end: Optional[date] = None,
                         sender_id: Optional[int] = None,
                         receiver_id: Optional[int] = None,
                         direction: Optional[str] = None,
                         sort_by: Optional[str] = None) -> List[Transactions]:
    offset = (page - 1) * page_size

    sql_query = '''
    SELECT id, is_recurring, amount, status, message, transaction_date, recurring_date, wallet_id, receiver_id
    FROM transactions
    WHERE 1=1
    '''
    params = []

    if period_start is not None:
        sql_query += ' AND transaction_date >= %s'
        params.append(period_start)
    if period_end is not None:
        sql_query += ' AND transaction_date <= %s'
        params.append(period_end)
    if sender_id:
        sql_query += ' AND wallet_id = %s'
        params.append(sender_id)
    if receiver_id:
        sql_query += ' AND receiver_id = %s'
        params.append(receiver_id)
    if direction:
        if direction == 'incoming':
            sql_query += ' AND receiver_id IS NOT NULL'
        elif direction == 'outgoing':
            sql_query += ' AND receiver_id IS NULL'
    if sort_by:
        sql_query += f' ORDER BY {sort_by}'
    
    sql_query += ' LIMIT %s OFFSET %s'
    params.extend([page_size, offset])

    data = read_query(sql_query, params)
    transactions = [Transactions.from_query_result(*row) for row in data]
    
    return transactions

def get_pending_transactions():
    transactions = []

    data =  read_query('''
    SELECT id, is_recurring, amount, status, message, transaction_date, recurring_date, wallet_id, receiver_id
    FROM transactions
    WHERE status = 'pending'
    ''')

    for row in data:
        transaction = {
            'id': row[0],
            'is_recurring': row[1],
            'amount': row[2],
            'status': row[3],
            'message': row[4],
            'transaction_date': row[5],
            'recurring_date': row[6],
            'wallet_id': row[7],
            'receiver_id': row[8]
        }
        transactions.append(transaction)

    return transactions


def get_all_users(page: int = 1):
    page_size = 10
    offset = (page - 1) * page_size
    data = read_query(
        '''SELECT username FROM users
           LIMIT %s OFFSET %s''',
        (page_size, offset)
    )

    usernames = [row[0] for row in data]
    return usernames


def get_user(search_type: str, search_value: str):
    if search_type == 'id':
        query = '''
        SELECT id, username, first_name, last_name, email, phone_number, role, hashed_password, is_blocked
        FROM users
        WHERE id = %s
        '''
    elif search_type == 'username':
        query = '''
        SELECT id, username, first_name, last_name, email, phone_number, role, hashed_password, is_blocked
        FROM users
        WHERE username = %s
        '''
    elif search_type == 'email':
        query = '''
        SELECT id, username, first_name, last_name, email, phone_number, role, hashed_password, is_blocked
        FROM users
        WHERE email = %s
        '''
    elif search_type == 'phone':
        query = '''
        SELECT id, username, first_name, last_name, email, phone_number, role, hashed_password, is_blocked
        FROM users
        WHERE phone_number = %s
        '''
    else:
        raise ValueError("Invalid search type. Must be one of 'id', 'username', 'email', or 'phone'.")
    
    data = read_query(query, (search_value,))
    return [User.from_query_result(*row) for row in data]


def deny_pending_transaction(transaction_id: int):
    try:
        update_query('''
        UPDATE transactions
        SET status = 'denied'
        WHERE id = %s AND status = 'pending'
        ''', (transaction_id,))
    except Exception as e:
        raise e