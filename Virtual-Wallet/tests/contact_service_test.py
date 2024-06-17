import pytest
from fastapi import HTTPException
from unittest.mock import patch
from services import contact_service
from data_.models import User, Wallet, ContactList, ExternalContacts, ViewContacts, AccountDetails

@pytest.fixture
def mock_user():
    return User(id=999, username='testuser', password='hashed_password', first_name='Test', last_name='User', email='testuser@example.com', phone_number='1234567890', role='user', is_blocked=False)

@pytest.fixture
def mock_contact_user():
    return User(id=1000, username='contactuser', password='hashed_password', first_name='Contact', last_name='User', email='contactuser@example.com', phone_number='0987654321', role='user', is_blocked=False)

@pytest.fixture
def mock_external_contact():
    return ExternalContacts(contact_name='External Contact', contact_email='external@example.com', iban='BG80BNBG96611020345678')

@pytest.fixture
def mock_contact_list(mock_user, mock_contact_user):
    return ContactList(id=1, user_id=mock_user.id, contact_id=mock_contact_user.id)

@pytest.fixture
def mock_external_contact_list(mock_user, mock_external_contact):
    return ContactList(id=2, user_id=mock_user.id, external_user_id=1)

def test_get_username_by(mocker):
    mock_user_data = [('testuser',)]

    mocker.patch('services.contact_service.read_query', return_value=mock_user_data)

    result = contact_service.get_username_by(999, 'test')

    assert result == {1: 'testuser'}

def test_view_user_contacts(mocker, mock_user):
    mock_contacts = [(1, 'contactuser', 'contact@example.com', '1234567890')]

    mocker.patch('services.contact_service.read_query', return_value=mock_contacts)

    result = contact_service.view_user_contacts(mock_user.id)

    assert result == [ViewContacts(id=1, contact_name='contactuser', email='contact@example.com', phone_or_iban='1234567890')]

def test_add_user_to_contacts(mocker, mock_user, mock_contact_user):
    mock_user_data = [(mock_contact_user.id, mock_contact_user.username, mock_contact_user.first_name,
                       mock_contact_user.last_name, mock_contact_user.email, mock_contact_user.phone_number,
                       mock_contact_user.role, mock_contact_user.password, mock_contact_user.is_blocked)]
    mocker.patch('services.user_service.find_by_username', return_value=mock_contact_user)
    mocker.patch('services.contact_service.read_query', return_value=[])
    mocker.patch('services.contact_service.insert_query', return_value=1)
    mocker.patch('services.user_service.read_query', return_value=mock_user_data)

    result = contact_service.add_user_to_contacts(mock_user.id, mock_contact_user.username)

    assert result == ContactList(id=1, user_id=mock_user.id, contact_id=mock_contact_user.id)

def test_add_user_to_contacts_existing(mocker, mock_user, mock_contact_user):
    mocker.patch('services.user_service.find_by_username', return_value=mock_contact_user)
    mocker.patch('services.contact_service.read_query', return_value=[(1,)])

    with pytest.raises(HTTPException) as exc_info:
        contact_service.add_user_to_contacts(mock_user.id, mock_contact_user.username)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "No such user"

def test_add_external_user_to_contacts(mocker, mock_user, mock_external_contact):
    mocker.patch('services.contact_service.read_query', return_value=[])
    mocker.patch('services.contact_service.insert_query', side_effect=[1, 2])

    result = contact_service.add_external_user_to_contacts(mock_user.id, mock_external_contact)

    assert result == ContactList(id=2, user_id=mock_user.id, external_user_id=1)

def test_remove_from_contacts(mocker, mock_user, mock_contact_list):
    mocker.patch('services.contact_service.read_query', side_effect=[
        [(mock_contact_list.id, None)],
        [(mock_contact_list.id, None)]
    ])
    mocker.patch('services.contact_service.update_query', return_value=None)

    result = contact_service.remove_from_contacts(mock_user.id, mock_contact_list.contact_id)

    assert result is True

def test_remove_from_contacts_not_found(mocker, mock_user):
    mocker.patch('services.contact_service.read_query', return_value=[])

    with pytest.raises(HTTPException) as exc_info:
        contact_service.remove_from_contacts(mock_user.id, 9999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Contact not found in your contact list."

def test_get_contact_list(mocker, mock_user, mock_external_contact_list):
    mocker.patch('services.contact_service.read_query', return_value=[
        (mock_external_contact_list.id, mock_user.id, mock_external_contact_list.external_user_id)
    ])

    result = contact_service.get_contact_list(mock_user, 'External Contact')

    assert result == ContactList(id=mock_external_contact_list.id, user_id=mock_user.id, external_user_id=1)

def test_get_contact_list_no_data(mocker, mock_user):
    mocker.patch('services.contact_service.read_query', return_value=[])

    result = contact_service.get_contact_list(mock_user, [])

    assert result is None

def test_get_user_contact_list(mocker, mock_user, mock_contact_list):
    mocker.patch('services.contact_service.read_query', return_value=[
        (mock_contact_list.id, mock_user.id, mock_contact_list.contact_id)
    ])

    result = contact_service.get_user_contact_list(mock_user, 'contactuser')

    assert result == ContactList(
        id=mock_contact_list.id,
        user_id=mock_user.id,
        contact_id=None,
        external_user_id=mock_contact_list.contact_id
    )

def test_get_user_contact_list_no_data(mocker, mock_user):
    mocker.patch('services.contact_service.read_query', return_value=[])

    result = contact_service.get_user_contact_list(mock_user, [])

    assert result is None


