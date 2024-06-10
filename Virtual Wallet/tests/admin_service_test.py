import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


<<<<<<< Updated upstream
if __name__ == '__main__':
    unittest.main()
=======
@patch('services.admin_service.read_query')
def test_block_user_user_not_found(mock_read_query):
    mock_read_query.return_value = []
    
    with pytest.raises(ValueError, match='No user found with id 1'):
        block_user(1)
    
    mock_read_query.assert_called_once_with("SELECT id FROM users WHERE id = ?", (1,))


@patch('services.admin_service.read_query')
@patch('services.admin_service.update_query')
def test_unblock_user_success(mock_update_query, mock_read_query):
    mock_read_query.return_value = [(1,)]
    mock_update_query.return_value = None
    
    result = unblock_user(1)
    
    assert result == 'User unblocked successfully!'
    
    mock_read_query.assert_called_once_with("SELECT id FROM users WHERE id = ?", (1,))
    mock_update_query.assert_called_once_with("UPDATE users SET is_blocked = 0 WHERE id = ?", (1,))


@patch('services.admin_service.read_query')
def test_unblock_user_user_not_found(mock_read_query):
    mock_read_query.return_value = []
    
    with pytest.raises(ValueError, match='No user found with id 1'):
        unblock_user(1)
    
    mock_read_query.assert_called_once_with("SELECT id FROM users WHERE id = ?", (1,))


@patch('services.admin_service._get_connection')
def test_approve_user_success(mock_get_connection):
    mock_cursor = mock_get_connection.return_value.cursor.return_value
    
    approve_user(1)
    
    mock_cursor.execute.assert_called_once_with(
        "UPDATE users SET is_blocked = 0 WHERE id = ?",
        (1,)
    )
    
    assert mock_get_connection.return_value.commit.called
    assert mock_get_connection.return_value.close.called


@patch('services.admin_service.read_query')
def test_get_all_transactions_no_filters(mock_read_query):
    mock_read_query.return_value = [(1, True, 100, 'completed', 'test', None, None, date(2024, 6, 1), 1, 2, 3)]
    
    transactions = get_all_transactions()
    
    assert len(transactions) == 1
    assert transactions[0].id == 1


@patch('services.admin_service.read_query')
def test_get_all_transactions_with_start_date(mock_read_query):
    mock_read_query.return_value = [(1, True, 100, 'completed', 'test', None, None, date(2024, 6, 1), 1, 2, 3)]
    
    start_date = date(2024, 6, 1)
    transactions = get_all_transactions(period_start=start_date)
    
    assert len(transactions) == 1
    assert transactions[0].id == 1


@patch('services.admin_service.read_query')
def test_get_all_incoming_transactions(mock_read_query):
    mock_read_query.return_value = [(1, True, 100, 'completed', 'test', None, None, date(2024, 6, 1), 1, 2, 3)]
    
    transactions = get_all_transactions(direction='incoming')
    
    assert len(transactions) == 1
    assert transactions[0].id == 1


@patch('services.admin_service.read_query')
def test_get_all_transactions_with_sender_id(mock_read_query):
    mock_read_query.return_value = [(1, True, 100, 'completed', 'test', None, None, date(2024, 6, 1), 1, 2, 3)]
    
    sender_id = 1
    transactions = get_all_transactions(sender_id=sender_id)
    
    assert len(transactions) == 1
    assert transactions[0].id == 1


@patch('services.admin_service.read_query')
def test_get_all_transactions_with_receiver_id(mock_read_query):
    mock_read_query.return_value = [(1, True, 100, 'completed', 'test', None, None, date(2024, 6, 1), 1, 2, 3)]
    
    receiver_id = 2
    transactions = get_all_transactions(receiver_id=receiver_id)
    
    assert len(transactions) == 1
    assert transactions[0].id == 1


@patch('services.admin_service.read_query')
def test_get_pending_transactions(mock_read_query):
    mock_read_query.return_value = [
        (1, True, 100, 'pending', 'test', '2024-06-01', None, 1, 2),
    ]
    
    pending_transactions = get_pending_transactions()
    
    assert len(pending_transactions) == 1
    assert pending_transactions[0]['id'] == 1
    assert pending_transactions[0]['status'] == 'pending'


@patch('services.admin_service.read_query')
def test_get_all_users(mock_read_query):
    mock_read_query.return_value = [('user1',), ('user2',), ('user3',)]
    
    usernames = get_all_users(page=1)
    
    assert len(usernames) == 3
    assert usernames == ['user1', 'user2', 'user3']


@patch('services.admin_service.read_query')
def test_get_user_by_id(mock_read_query):
    mock_read_query.return_value = [(1, 'user1', 'niksun', 'stan', 'test@example.com', '1234567890', 'user', 'hashed_password', False)]
    
    user = get_user(search_type='id', search_value='1')
    

    assert len(user) == 1
    assert user[0].id == 1
    assert user[0].username == 'user1'


@patch('services.admin_service.read_query')
def test_get_user_by_username(mock_read_query):
    mock_read_query.return_value = [(2, 'user2', 'nik', 'sta', 'test@example.com', '0987654321', 'admin', 'hashed_password', True)]
    user = get_user(search_type='username', search_value='user2')
    assert len(user) == 1
    assert user[0].id == 2
    assert user[0].email == 'test@example.com'
    assert user[0].role == 'admin'


@patch('services.admin_service.read_query')
def test_get_user_by_email(mock_read_query):
    mock_read_query.return_value = [(3, 'user3', 'niki', 'stanko', 'test@example.com', '0887889966', 'user', 'hashed_password', False)]
    user = get_user(search_type='email', search_value='test@example.com')
    assert len(user) == 1
    assert user[0].id == 3
    assert user[0].role == 'user'


@patch('services.admin_service.read_query')
def test_get_user_by_phone(mock_read_query):
    mock_read_query.return_value = [(4, 'user4', 'nikito', 'stanko', 'test@example.com', '0889445566', 'user', 'hashed_password', False)]
    user = get_user(search_type='phone', search_value='0889445566')
    assert len(user) == 1
    assert user[0].id == 4
    assert user[0].first_name == 'nikito'


@patch('services.admin_service.update_query')
def test_deny_pending_transaction(mock_update_query):
    mock_update_query.return_value = None
    
    deny_pending_transaction(transaction_id=1)
    
    mock_update_query.assert_called_once_with('''
        UPDATE transactions
        SET status = 'denied'
        WHERE id = %s AND status = 'pending'
        ''', (1,))
>>>>>>> Stashed changes
