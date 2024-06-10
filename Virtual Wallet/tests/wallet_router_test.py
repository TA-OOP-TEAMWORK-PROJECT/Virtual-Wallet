import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app
from data_.models import User
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


def test_get_balance(override_get_current_active_user):
    with patch('routers.wallet_router.get_wallet_balance', new=MagicMock(return_value={'balance': 1500.0})):
        response = client.get("/wallets/balance")
    assert response.status_code == 200
    assert response.json() == {'balance': 1500.0}


def test_topup_wallet(override_get_current_active_user):
    with patch('routers.wallet_router.add_money_to_wallet', new=MagicMock(return_value={'balance': 1000.0})):
        response = client.post("/wallets/top-up", params={"card_id": 2, "amount": 500.0})
    assert response.status_code == 200
    assert response.json() == {'balance': 1000.0}


def test_withdraw_money(override_get_current_active_user):
    with patch('routers.wallet_router.withdraw_money_from_wallet', new=MagicMock(return_value={'balance': 500.0})):
        response = client.post("/wallets/withdraw", params={"card_id": 2, "amount": 500.0})
    assert response.status_code == 200
    assert response.json() == {'balance': 500.0}


def test_topup_wallet_virtual_card(override_get_current_active_user):
    with patch('routers.wallet_router.add_money_to_wallet', new=MagicMock(side_effect=HTTPException(status_code=400, detail="Cannot use a virtual card for top-up."))):
        response = client.post("/wallets/top-up", params={"card_id": 1001, "amount": 500.0})
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot use a virtual card for top-up."}


def test_withdraw_money_virtual_card(override_get_current_active_user):
    with patch('routers.wallet_router.withdraw_money_from_wallet', new=MagicMock(side_effect=HTTPException(status_code=400, detail="Cannot use a virtual card for withdrawal."))):
        response = client.post("/wallets/withdraw", params={"card_id": 1001, "amount": 500.0})
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot use a virtual card for withdrawal."}