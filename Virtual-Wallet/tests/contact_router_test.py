import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app
from data_.models import User, ExternalContacts, ContactList, ViewContacts
from common.auth import get_current_active_user

client = TestClient(app)


@pytest.fixture
def mock_user():
    return User(id=1, username='testuser', first_name='Test', last_name='User', email='test@example.com', phone_number='1234567890', role='user', is_blocked=False)


@pytest.fixture
def override_get_current_active_user(mock_user):
    async def mock_get_current_active_user():
        return mock_user
    app.dependency_overrides[get_current_active_user] = mock_get_current_active_user
    yield
    app.dependency_overrides.pop(get_current_active_user, None)


def test_view_contacts_list(override_get_current_active_user):
    mock_contacts = [
        ViewContacts(id=1, contact_name='contactuser', email='contact@example.com', phone_or_iban='1234567890')
    ]

    with patch('routers.contact_router.view_user_contacts', new=MagicMock(return_value=mock_contacts)):
        response = client.get("/contacts/")

    assert response.status_code == 200
    assert response.json() == [contact.dict() for contact in mock_contacts]


def test_search_contacts(override_get_current_active_user):
    mock_search_results = {1: 'contactuser'}

    with patch('routers.contact_router.get_username_by', new=MagicMock(return_value=mock_search_results)):
        response = client.get("/contacts/search", params={"search": "contact", "contact_list": False})

    assert response.status_code == 200
    expected_result = {str(k): v for k, v in mock_search_results.items()}
    assert response.json() == expected_result


def test_add_contact(override_get_current_active_user):
    mock_contact = ContactList(id=1, user_id=1, contact_id=2)

    with patch('routers.contact_router.add_user_to_contacts', new=MagicMock(return_value=mock_contact)):
        response = client.post("/contacts/add", params={"contact_request": "contact_id_2"})

    assert response.status_code == 200
    assert response.json() == mock_contact.dict()

def test_add_external_contact(override_get_current_active_user):
    mock_contact = ContactList(id=1, user_id=1, external_user_id=1)
    mock_external_data = ExternalContacts(contact_name='External Contact', contact_email='external@example.com', iban='BG80BNBG96611020345678')

    with patch('routers.contact_router.add_external_user_to_contacts', new=MagicMock(return_value=mock_contact)):
        response = client.post("/contacts/add/external", json=mock_external_data.dict())

    assert response.status_code == 200
    assert response.json() == mock_contact.dict()


def test_remove_contact(override_get_current_active_user):
    with patch('routers.contact_router.remove_from_contacts', new=MagicMock(return_value=True)):
        response = client.delete("/contacts/remove", params={"removed_user_id": 2})

    assert response.status_code == 200
    assert response.json() == "Contact removed successfully."












