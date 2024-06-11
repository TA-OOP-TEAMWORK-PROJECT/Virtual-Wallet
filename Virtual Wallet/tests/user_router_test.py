from unittest.mock import MagicMock, patch
from data_.models import User, AccountDetails, UserCreate, UserUpdate
from tests.mock_users_data import authorized_client, mock_user, regular_token, client

def test_read_users_me(authorized_client, mock_user): #
    with patch('services.user_service.find_by_username', return_value=mock_user):
        with patch('routers.user_router.get_user_response', return_value={
            "id": 1,
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone_number": "1234567890",
            "role": "user",
            "is_blocked": False
        }):
            response = authorized_client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone_number": "1234567890",
        "role": "user",
        "is_blocked": False
    }

def test_get_account_details(authorized_client, mock_user):
    mock_account_details = AccountDetails(
        user={'username': 'testuser', 'first_name': 'Test', 'last_name': 'User', 'email': 'test@example.com', 'phone_number': '1234567890'},
        wallet={'user_id': 1, 'amount': 1000.0},
        cards=[],
        categories=[],
        contacts=[],
        transactions=[]
    )
    with patch('services.user_service.find_by_username', return_value=mock_user):
        with patch('routers.user_router.user_service.get_user_account_details', return_value=mock_account_details):
            response = authorized_client.get("/users/details")
    assert response.status_code == 200
    assert response.json() == mock_account_details.dict()

def test_register_user():
    user_data = UserCreate(
        username="newuser",
        password="password123",
        first_name="New",
        last_name="User",
        email="newuser@example.com",
        phone_number="0987654321"
    )
    with patch('routers.user_router.user_service.create', new=MagicMock(return_value=User(**user_data.dict(), id=2, role="user", is_blocked=False, hashed_password='hashedpassword'))):
        response = client.post("/users/register", json=user_data.dict())
    assert response.status_code == 200
    assert response.json() == {'message': 'User with username newuser has been created and awaits approval!'}

def test_login_for_access_token(mock_user):
    form_data = {
        "username": "testuser",
        "password": "passworD123+"
    }
    with patch('services.user_service.find_by_username', new=MagicMock(return_value=mock_user)):
        with patch('common.auth.authenticate_user', new=MagicMock(return_value=mock_user)):
            with patch('common.auth.create_access_token', new=MagicMock(return_value="testtoken")):
                response = client.post("/users/login", data=form_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"

def test_update_user_profile(authorized_client, mock_user):
    user_update = UserUpdate(
        email="updateduser@example.com",
        phone_number="1231231234",
        password="newpassword123"
    )
    with patch('services.user_service.find_by_username', return_value=mock_user):
        with patch('routers.user_router.user_service.update_user_profile', new=MagicMock(return_value="Profile updated successfully.")):
            response = authorized_client.put("/users/update", json=user_update.dict())
    assert response.status_code == 200
    assert response.json() == {"message": "Profile updated successfully."}





