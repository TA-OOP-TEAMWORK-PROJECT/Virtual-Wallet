from datetime import date

import pytest

from data_.models import Wallet, User, Transactions, TransferConfirmation, ContactList, ExternalContacts, UserTransfer, \
    RecurringTransaction
from services import transaction_service
from services.transaction_service import get_transactions
from fastapi import HTTPException, Response


@pytest.fixture
def mock_user_wallet():
    return Wallet(id=1, amount=1000, user_id=1)

@pytest.fixture
def mock_user():
    return User(id = 1, username= 'ikonata', first_name = 'Valeri', last_name = 'Bojinov',
                email = 'testmail@teenproblem.com', phone_number='0897045023')

@pytest.fixture
def mock_contact_list():
    return ContactList(id=4, user_id=1, external_user_id=2)


def test_get_transactions_no_search(mocker, mock_user_wallet, mock_user):
    ''' [(id, is_recurring, status, amount, transaction_date, receiver_id, contact_list_id, recurring_date)] '''
    mock_transaction_data = [(5, 1, 'confirmed', 100, date(2024, 6, 9), 2, None, None)]

    mocker.patch('services.transaction_service.find_wallet_id', return_value = mock_user_wallet)
    mocker.patch('services.transaction_service.read_query', return_value = mock_transaction_data)

    result = transaction_service.get_transactions(mock_user, None)

    assert result == [Transactions(id=5, is_recurring=True, amount=100.0, status='confirmed', message=None,
                    recurring_pereiod = None, recurring_date=None, transaction_date=date(2024, 6, 9),
                    wallet_id=None, receiver_id=2, contact_list_id=None, category_id=None)]


def test_get_transactions_when_search_is_set(mocker, mock_user_wallet, mock_user):
    ''' [(id, is_recurring, status, amount, transaction_date, receiver_id, contact_list_id, recurring_date)] '''
    mock_transaction_data = [(5, 1, 'confirmed', 100, date(2024, 6, 9), 2, None, None)]

    mocker.patch('services.transaction_service.find_wallet_id', return_value = mock_user_wallet)
    mocker.patch('services.transaction_service.read_query', return_value = mock_transaction_data)

    result = transaction_service.get_transactions(mock_user, '2024-06-09')

    assert result == [Transactions(id=5, is_recurring=True, amount=100.0, status='confirmed', message=None,
                    recurring_pereiod = None, recurring_date=None, transaction_date=date(2024, 6, 9),
                    wallet_id=None, receiver_id=2, contact_list_id=None, category_id=None)]


def test_view_all_recurring_transactions(mocker, mock_user, mock_user_wallet):

    mock_transaction_data = [( 1, 100, 30, date(2024, 7, 9), date(2024, 6, 9), 3, 2)]

    mocker.patch('services.transaction_service.get_user_wallet', return_value=mock_user_wallet)
    mocker.patch('services.transaction_service.read_query', return_value=mock_transaction_data)

    result = transaction_service.view_all_recuring_transactions(mock_user)

    assert {1: {'Amount': 100.0, 'Date of next transfer': date(2024, 7, 9), 'Last transfer date': date(2024, 6, 9), 'Status': 'pending'}}


def test_sort_transactions():

    mock_transaction_data = [
        Transactions(id=3, is_recurring=0, amount=2.20,status='confirmed',message='Za semki',
        transaction_date=date(2024, 6, 9),wallet_id=1, receiver_id=2),
        Transactions(id=1, is_recurring=0, amount=20.20, status='pending', message='To have',
                     transaction_date=date(2023, 6, 9), wallet_id=1, receiver_id=2)
    ]

    result = transaction_service.sort_transactions(mock_transaction_data, 'transaction_date', False)

    assert [
        Transactions(id=1, is_recurring=False, amount=20.2, status='pending', message='To have', recurring_period=None,recurring_date=None,
                transaction_date=date(2023, 6, 9), wallet_id=1, receiver_id=2, contact_list_id=None, category_id=None),
        Transactions(id=3, is_recurring=False, amount=2.2, status='confirmed', message='Za semki', recurring_period=None, recurring_date=None,
                     transaction_date=date(2024, 6, 9), wallet_id=1, receiver_id=2, contact_list_id=None, category_id=None)]


def test_in_app_transfer_when_receiver_data_and_user_in_contact_list(mocker, mock_user):
    '''id, username, first_name, last_name,email, phone_number, role, hashed_password, is_blocked'''

    mock_transaction_data = [(
        2, 'gosho123', 'Georgi', 'Ivanov', 'testmail@teenproblem.com',
        '0897456525', 'user', '$2b$12$t6.YYwDAFyf/9WAa8I7/xuCr40I42RviZdd3hR7.Z1nRLPTzxT5wC', False
    )]

    mocker.patch('services.transaction_service.read_query', return_value=mock_transaction_data)
    mocker.patch('services.transaction_service.check_contact_list', return_value=True)
    mocker.patch('services.transaction_service.user_transfer', return_value=HTTPException(status_code=200,
                detail=f'The amount of 100 was sent.'))

    result = transaction_service.in_app_transfer({'amount':100}, '0897456525', mock_user)

    assert result.status_code == 200
    assert result.detail == 'The amount of 100 was sent.'

def test_in_app_transfer_when_receiver_data_and_user_in_contact_list(mocker, mock_user):

    mock_transaction_data = [(
        2, 'gosho123', 'Georgi', 'Ivanov', 'testmail@teenproblem.com',
        '0897456525', 'user', '$2b$12$t6.YYwDAFyf/9WAa8I7/xuCr40I42RviZdd3hR7.Z1nRLPTzxT5wC', False
    )]

    mock_transfer_message = (
        TransferConfirmation(
                            new_wallet_amount=1000,
                            receiver_wallet_amount=1200,
                            transaction_amount=100,
                            transaction_date=date.today(),
                            wallet_id=1,
                            receiver_wallet_id=2,
                            user_id=1,
                            receiver_id=2,
                            is_external=False))

    mocker.patch('services.transaction_service.read_query', return_value=mock_transaction_data)
    mocker.patch('services.transaction_service.check_contact_list', return_value=False)
    mocker.patch('services.transaction_service.user_transfer', return_value=mock_transfer_message)

    result = transaction_service.in_app_transfer({'amount': 100}, '0897456525', mock_user)

    assert TransferConfirmation(
                            new_wallet_amount=1000,
                            receiver_wallet_amount=1200,
                            transaction_amount=100,
                            transaction_date=date.today(),
                            wallet_id=1,
                            receiver_wallet_id=2,
                            user_id=1,
                            receiver_id=2,
                            is_external=False)


def test_in_app_transfer_when_receiver_data_is_none(mocker, mock_user):

    mock_transaction_data = None

    mocker.patch('services.transaction_service.read_query', return_value=mock_transaction_data)
    result = transaction_service.in_app_transfer(mock_transaction_data, '0897456525', mock_user)

    assert result.status_code == 404
    assert result.body == b'There is no user with the given credentials'


def test_bank_transfer_when_wallet_amount_is_enough(mocker, mock_user_wallet, mock_user, mock_contact_list):


    mock_external_user = ExternalContacts(
        id=3, contact_name='CHEZ',contact_email='examplemail@teenproblem.com',
        iban='4567fse896542s4w85d25d')

    mocker.patch('services.transaction_service.get_contact_list', return_value=mock_contact_list)
    mocker.patch('services.transaction_service.get_user_wallet', return_value=mock_user_wallet)

    result = transaction_service.bank_transfer(mock_external_user, UserTransfer(amount=100), mock_user)
    assert TransferConfirmation(
        new_wallet_amount=900.0, receiver_wallet_amount=None, transaction_amount=100.0,
        transaction_date=date(2024, 6, 10), wallet_id=1, receiver_wallet_id=None,
        user_id=None, receiver_id=4, is_external=True)



def test_bank_transfer_when_wallet_amount_is_not_enough(mocker, mock_user_wallet, mock_user, mock_contact_list):

    mock_external_user = ExternalContacts(
        id=3, contact_name='CHEZ',contact_email='examplemail@teenproblem.com',
        iban='4567fse896542s4w85d25d')

    mocker.patch('services.transaction_service.get_contact_list', return_value=mock_contact_list)
    mocker.patch('services.transaction_service.get_user_wallet', return_value=mock_user_wallet)

    with pytest.raises(HTTPException) as exc_info:
        transaction_service.bank_transfer(mock_external_user, UserTransfer(amount=10000), mock_user)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Insufficient funds'


def test_external_recurring_transaction_when_wallet_amount_is_enough(mocker, mock_user_wallet, mock_user, mock_contact_list):

    mock_recurring_transaction = RecurringTransaction(
        id=5, amount=100.0, recurring_period=30,recurring_date=date(2025, 6, 8),
        transaction_date=date(2024, 6, 8), contact_list_id=1)
    mock_external_user = ExternalContacts(
        id=3, contact_name='CHEZ', contact_email='examplemail@teenproblem.com',
        iban='4567fse896542s4w85d25d')

    mocker.patch('services.transaction_service.get_contact_list', return_value=mock_contact_list)
    mocker.patch('services.transaction_service.get_user_wallet', return_value=mock_user_wallet)
    mocker.patch('services.transaction_service.insert_query', return_value=1)

    result = transaction_service.external_recurring_transaction(mock_recurring_transaction, mock_external_user, mock_user)

    assert {
        'You have set a new recurring transaction:':
            {
                'Contact name is': 'CHEZ',
                'Next payment day': date(2025, 6, 8),
                'Payment period is': 30,
                'Transaction amount': 100.0
            }
    }

def test_external_recurring_transaction_when_wallet_amount_is_not_enough(mocker, mock_user_wallet, mock_user, mock_contact_list):

    mock_recurring_transaction = RecurringTransaction(
        id=5, amount=10000.0, recurring_period=30,recurring_date=date(2025, 6, 8),
        transaction_date=date(2024, 6, 8), contact_list_id=1)
    mock_external_user = ExternalContacts(
        id=3, contact_name='CHEZ', contact_email='examplemail@teenproblem.com',
        iban='4567fse896542s4w85d25d')

    mocker.patch('services.transaction_service.get_contact_list', return_value=mock_contact_list)
    mocker.patch('services.transaction_service.get_user_wallet', return_value=mock_user_wallet)
    mocker.patch('services.transaction_service.insert_query', return_value=1)

    with pytest.raises(HTTPException) as exc_info:
        transaction_service.external_recurring_transaction(mock_recurring_transaction, mock_external_user, mock_user)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == 'Not enough funds to complete the transaction'

