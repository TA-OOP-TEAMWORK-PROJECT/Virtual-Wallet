from services import user_service
from services.user_service import find_by_username
from data_.models import User, UserUpdate, AccountDetails, Card, Wallet, Categories, ContactList, ExternalContacts, \
    Transactions
from fastapi import HTTPException
import pytest


def test_create_user_success(mocker):
    mocker.patch('services.user_service.auth.get_password_hash', return_value='hashed_password')
    mocker.patch('services.user_service.insert_query', side_effect=[1, None])
    mocker.patch('services.user_service.send_registration_email')
    mocker.patch('services.user_service.check_if_unique', return_value=None)

    user = user_service.create('username', 'Password1+', 'First', 'Last', 'email@example.com', '1234567890')

    assert user.id == 1
    assert user.username == 'username'
    assert user.password == 'Password1+'
    assert user.first_name == 'First'
    assert user.last_name == 'Last'
    assert user.email == 'email@example.com'
    assert user.phone_number == '1234567890'


def test_create_user_duplicate_username(mocker):
    mocker.patch('services.user_service.check_if_unique',
                 side_effect=HTTPException(status_code=400, detail='Username username is taken.'))

    with pytest.raises(HTTPException) as exc_info:
        user_service.create('username', 'Password1+', 'First', 'Last', 'email@example.com', '1234567890')

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Username username is taken.'


def test_find_by_username_success(mocker):
    user_data = [(1, 'username', 'First', 'Last', 'email@example.com', '1234567890', 'user', 'hashed_password', False)]
    mocker.patch('services.user_service.read_query', return_value=user_data)

    user = user_service.find_by_username('username')

    assert user.username == 'username'


def test_find_by_username_not_found(mocker):
    mocker.patch('services.user_service.read_query', return_value=[])

    user = user_service.find_by_username('username')

    assert user is None


def test_find_by_phone_number_success(mocker):
    user_data = [(1, 'username', 'First', 'Last', 'email@example.com', '1234567890', 'user', 'hashed_password', False)]
    mocker.patch('services.user_service.read_query', return_value=user_data)

    user = user_service.find_by_phone_number('1234567890')

    assert user.phone_number == '1234567890'


def test_find_by_phone_number_not_found(mocker):
    mocker.patch('services.user_service.read_query', return_value=[])

    user = user_service.find_by_phone_number('1234567890')

    assert user is None


def test_find_by_id_success(mocker):
    user_data = [(1, 'username', 'First', 'Last', 'email@example.com', '1234567890', 'user', 'hashed_password', False)]
    mocker.patch('services.user_service.read_query', return_value=user_data)

    user = user_service.find_by_id(1)

    assert user.id == 1


def test_find_by_id_not_found(mocker):
    mocker.patch('services.user_service.read_query', return_value=[])

    user = user_service.find_by_id(1)

    assert user is None


def test_update_user_profile_success(mocker):
    user_data = [(1, 'username', 'First', 'Last', 'email@example.com', '1234567890', 'user', 'hashed_password', False)]
    mocker.patch('services.user_service.find_by_username', return_value=User.from_query_result(*user_data[0]))
    mocker.patch('services.user_service.update_query')
    mocker.patch('services.user_service.check_if_unique', return_value=None)

    user_update = UserUpdate(email='new_email@example.com', phone_number='0987654321', password='NewPassword1+')
    message = user_service.update_user_profile('username', user_update)

    assert message == "User 'username' successfully updated their: email from email@example.com to new_email@example.com, phone number from 1234567890 to 0987654321, password."


def test_update_user_profile_no_changes(mocker):
    user_data = [(1, 'username', 'First', 'Last', 'email@example.com', '1234567890', 'user', 'hashed_password', False)]
    mocker.patch('services.user_service.find_by_username', return_value=User.from_query_result(*user_data[0]))

    user_update = UserUpdate(email='email@example.com', phone_number='1234567890', password=None)

    message = user_service.update_user_profile('username', user_update)
    assert message == "No changes detected."


def test_get_user_account_details(mocker):
    user_data = [(1, 'username', 'First', 'Last', 'email@example.com', '1234567890', 'user', 'hashed_password', False)]
    wallet_data = [(1, 100.0, 1)]
    card_data = [(1, '4242424242424242', '2025-01-01', 'First Last', '123', 1, False)]
    category_data = [(1, 'Category1', 1)]
    contact_data = [(1, 1, 2, None)]
    transaction_data = [(1, False, 100.0, 'confirmed', 'Payment', None, None, '2024-05-01', 1, 2, 1, 1)]

    mocker.patch('services.user_service.find_by_id', return_value=User.from_query_result(*user_data[0]))
    mocker.patch('services.user_service.get_user_wallet', return_value=Wallet.from_query_result(*wallet_data[0]))
    mocker.patch('services.user_service.get_user_cards', return_value=[Card.from_query_result(*card_data[0])])
    mocker.patch('services.user_service.get_user_categories',
                 return_value=[Categories.from_query_result(*category_data[0])])
    mocker.patch('services.user_service.get_user_contacts',
                 return_value=[ContactList.from_query_result(*contact_data[0])])
    mocker.patch('services.user_service.get_user_transactions',
                 return_value=[Transactions.from_query_result(*transaction_data[0])])

    account_details = user_service.get_user_account_details(1)

    assert account_details.user.id == 1
    assert account_details.wallet.amount == 100.0
    assert len(account_details.cards) == 1
    assert len(account_details.categories) == 1
    assert len(account_details.contacts) == 1
    assert len(account_details.transactions) == 1


def test_check_if_unique_username_taken(mocker):
    mocker.patch('services.user_service.read_query', return_value=[(1,)])

    with pytest.raises(HTTPException) as exc_info:
        user_service.check_if_unique(username='username')

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Username username is taken.'


def test_check_if_unique_email_taken(mocker):
    mocker.patch('services.user_service.read_query', return_value=[(1,)])

    with pytest.raises(HTTPException) as exc_info:
        user_service.check_if_unique(email='email@example.com')

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Email email@example.com is taken.'


def test_check_if_unique_phone_number_taken(mocker):
    mocker.patch('services.user_service.read_query', return_value=[(1,)])

    with pytest.raises(HTTPException) as exc_info:
        user_service.check_if_unique(phone_number='1234567890')

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Phone number 1234567890 is taken.'


def test_password_check_success():
    assert user_service.password_check('Password1+') == 'Password1+'


def test_password_check_no_digit():
    with pytest.raises(HTTPException) as exc_info:
        user_service.password_check('Password+')

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Password must contain at least one digit'


def test_password_check_no_uppercase():
    with pytest.raises(HTTPException) as exc_info:
        user_service.password_check('password1+')

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Password must contain at least one uppercase letter'


def test_password_check_no_lowercase():
    with pytest.raises(HTTPException) as exc_info:
        user_service.password_check('PASSWORD1+')

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Password must contain at least one lowercase letter'


def test_password_check_no_special_char():
    with pytest.raises(HTTPException) as exc_info:
        user_service.password_check('Password1')

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Password must contain at least one special character (+, -, *, ^, &)'

