
from data_.database import update_query, read_query

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