<<<<<<< Updated upstream
=======
import requests
from data_.database import update_query, read_query
from data_.database import _get_connection
from common.config import MAILJET_API_KEY, MAILJET_API_SECRET, ADMIN_EMAIL

def block_user(user_id: int):
    # проверка за юзъра
    user_result = read_query("SELECT id FROM users WHERE id = ?", (user_id,))
    if not user_result:
        raise ValueError(f'No user found with id {user_id}')

    # блокиране на юзъра
    update_query("UPDATE users SET is_blocked = 1 WHERE id = ?", (user_id,))
    
    return 'User blocked successfully'


def unblock_user(user_id: int):
    # проверка на юзъра
    user_result = read_query("SELECT id FROM users WHERE id = ?", (user_id,))
    if not user_result:
        raise ValueError(f'No user found with id {user_id}')

    
    # отблокиране на юзъра
    update_query("UPDATE users SET is_blocked = 0 WHERE id = ?", (user_id,))

    return 'User unblocked successfully!'


def send_registration_email(user_email):
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
                'TextPart': f'A new user has registered: {user_email}. Please review and approve the registration.',
                'HTMLPart': f'<h3>A new user has registered: {user_email}</h3><p>Please review and approve the registration.</p>'
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

>>>>>>> Stashed changes
