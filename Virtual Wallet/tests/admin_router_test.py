from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest
from main import app
from data_.models import User
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))


# app/main.py
from fastapi import FastAPI
from routers import admin_router

app = FastAPI()
app.include_router(admin_router.router)

@pytest.fixture
def client():
    return TestClient(app)

def test_get_all_users_route_success(client):
    mock_admin_user = User(id=1, username="admin", first_name="Admin", last_name="User", email="admin@example.com", phone_number="12345678", role="admin")

    with patch('your_module.get_current_admin_user', return_value=mock_admin_user), \
         patch('your_module.get_all_users', return_value=["username1", "username2"]):
        
        response = client.get('/users?page=1')

        assert response.status_code == 200
        assert response.json() == ["username1", "username2"]

def test_get_all_users_route_unauthorized(client):
    with patch('your_module.get_current_admin_user', return_value=None):
        response = client.get('/users?page=1')

        assert response.status_code == 401
        assert response.json() == {'detail': 'You are not authorized!'}

def test_get_all_users_route_forbidden(client):
    mock_non_admin_user = User(id=2, username="user", first_name="Regular", last_name="User", email="user@example.com", phone_number="12345678", role="user")

    with patch('your_module.get_current_admin_user', return_value=mock_non_admin_user):
        response = client.get('/users?page=1')

        assert response.status_code == 403
        assert response.json() == {'detail': 'Access denied'}

def test_get_all_users_route_exception(client):
    mock_admin_user = User(id=1, username="admin", first_name="Admin", last_name="User", email="admin@example.com", phone_number="12345678", role="admin")

    with patch('your_module.get_current_admin_user', return_value=mock_admin_user), \
         patch('your_module.get_all_users', side_effect=Exception("Database error")):
        
        response = client.get('/users?page=1')

        assert response.status_code == 500
        assert response.json() == {'detail': 'Database error'}
