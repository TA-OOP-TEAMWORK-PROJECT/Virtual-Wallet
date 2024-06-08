from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from datetime import timedelta
from main import app
from data_.models import User
from common.auth import create_access_token, pwd_context

client = TestClient(app)

@pytest.fixture
def mock_user():
    hashed_password = pwd_context.hash("passworD123+")
    return User(id=1, username='testuser', first_name='Test', last_name='User', email='test@example.com', phone_number='1234567890', role='user', is_blocked=False, hashed_password=hashed_password)

@pytest.fixture
def regular_token(mock_user):
    token_data = {'sub': mock_user.username, 'user_id': mock_user.id, 'role': mock_user.role}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=3000))

@pytest.fixture
def authorized_client(regular_token):
    client.headers.update({"Authorization": f"Bearer {regular_token}"})
    return client

@pytest.fixture(autouse=True)
def override_get_current_user(mock_user):
    with patch('common.auth.get_user', return_value=mock_user):
        yield