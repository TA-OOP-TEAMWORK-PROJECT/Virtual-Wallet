import pytest
from fastapi import HTTPException
from unittest.mock import patch
from services import wallet_service
from data_.models import Wallet, User

@pytest.fixture
def mock_user():
    return User(id=999, username='testuser', password='hashed_password', first_name='Test', last_name='User', email='testuser@example.com', phone_number='1234567890', role='user', is_blocked=False)

@pytest.fixture
def mock_wallet(mock_user):
    return Wallet(id=999, amount=50.0, user_id=mock_user.id)

@pytest.fixture
def mock_card():
    return [(999, False)]

def test_add_money_to_wallet_success(mocker, mock_wallet, mock_card):
    user_id = mock_wallet.user_id
    card_id = 999
    amount = 100.0

    mocker.patch('services.card_service.find_wallet_id', return_value=mock_wallet)
    mocker.patch('services.wallet_service.read_query', return_value=mock_card)
    mocker.patch('services.wallet_service.update_query', return_value=None)
    mocker.patch('services.card_service.read_query', return_value=[(mock_wallet.id, mock_wallet.amount, mock_wallet.user_id)])

    result = wallet_service.add_money_to_wallet(user_id, card_id, amount)

    assert result == "100.0 leva were successfully added to your wallet. Current balance = 150.0 leva."

def test_add_money_to_wallet_card_not_found(mocker, mock_wallet):
    user_id = mock_wallet.user_id
    card_id = 999
    amount = 100.0

    mocker.patch('services.card_service.find_wallet_id', return_value=mock_wallet)
    mocker.patch('services.wallet_service.read_query', return_value=[])
    mocker.patch('services.card_service.read_query', return_value=[(mock_wallet.id, mock_wallet.amount, mock_wallet.user_id)])

    with pytest.raises(HTTPException) as exc_info:
        wallet_service.add_money_to_wallet(user_id, card_id, amount)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Card not found."

def test_add_money_to_wallet_virtual_card(mocker, mock_wallet):
    user_id = mock_wallet.user_id
    card_id = 999
    amount = 100.0

    mock_virtual_card = [(card_id, True)]

    mocker.patch('services.card_service.find_wallet_id', return_value=mock_wallet)
    mocker.patch('services.wallet_service.read_query', return_value=mock_virtual_card)
    mocker.patch('services.card_service.read_query', return_value=[(mock_wallet.id, mock_wallet.amount, mock_wallet.user_id)])

    with pytest.raises(HTTPException) as exc_info:
        wallet_service.add_money_to_wallet(user_id, card_id, amount)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Cannot add money from a virtual card."

def test_add_money_to_wallet_non_positive_amount(mocker, mock_wallet, mock_card):
    user_id = mock_wallet.user_id
    card_id = 999
    amount = -10.0

    mocker.patch('services.card_service.find_wallet_id', return_value=mock_wallet)
    mocker.patch('services.wallet_service.read_query', return_value=mock_card)
    mocker.patch('services.card_service.read_query', return_value=[(mock_wallet.id, mock_wallet.amount, mock_wallet.user_id)])

    with pytest.raises(HTTPException) as exc_info:
        wallet_service.add_money_to_wallet(user_id, card_id, amount)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Amount must be greater than zero"

def test_withdraw_money_from_wallet_success(mocker, mock_wallet, mock_card):
    user_id = mock_wallet.user_id
    card_id = 999
    amount = 20.0

    mocker.patch('services.card_service.find_wallet_id', return_value=mock_wallet)
    mocker.patch('services.wallet_service.read_query', return_value=mock_card)
    mocker.patch('services.wallet_service.update_query', return_value=None)
    mocker.patch('services.card_service.read_query', return_value=[(mock_wallet.id, mock_wallet.amount, mock_wallet.user_id)])

    result = wallet_service.withdraw_money_from_wallet(user_id, card_id, amount)

    assert result == "20.0 leva were successfully withdrawn from your wallet. Current balance = 30.0 leva."

def test_withdraw_money_from_wallet_insufficient_funds(mocker, mock_wallet, mock_card):
    user_id = mock_wallet.user_id
    card_id = 999
    amount = 100.0

    mocker.patch('services.card_service.find_wallet_id', return_value=mock_wallet)
    mocker.patch('services.wallet_service.read_query', return_value=mock_card)
    mocker.patch('services.card_service.read_query', return_value=[(mock_wallet.id, mock_wallet.amount, mock_wallet.user_id)])

    with pytest.raises(HTTPException) as exc_info:
        wallet_service.withdraw_money_from_wallet(user_id, card_id, amount)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Insufficient funds in wallet"

def test_withdraw_money_from_wallet_card_not_found(mocker, mock_wallet):
    user_id = mock_wallet.user_id
    card_id = 999
    amount = 20.0

    mocker.patch('services.card_service.find_wallet_id', return_value=mock_wallet)
    mocker.patch('services.wallet_service.read_query', return_value=[])
    mocker.patch('services.card_service.read_query', return_value=[(mock_wallet.id, mock_wallet.amount, mock_wallet.user_id)])

    with pytest.raises(HTTPException) as exc_info:
        wallet_service.withdraw_money_from_wallet(user_id, card_id, amount)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Card not found."

def test_withdraw_money_from_wallet_virtual_card(mocker, mock_wallet):
    user_id = mock_wallet.user_id
    card_id = 999
    amount = 20.0

    mock_virtual_card = [(card_id, True)]

    mocker.patch('services.card_service.find_wallet_id', return_value=mock_wallet)
    mocker.patch('services.wallet_service.read_query', return_value=mock_virtual_card)
    mocker.patch('services.card_service.read_query', return_value=[(mock_wallet.id, mock_wallet.amount, mock_wallet.user_id)])

    with pytest.raises(HTTPException) as exc_info:
        wallet_service.withdraw_money_from_wallet(user_id, card_id, amount)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Cannot withdraw to a virtual card"

def test_withdraw_money_from_wallet_non_positive_amount(mocker, mock_wallet, mock_card):
    user_id = mock_wallet.user_id
    card_id = 999
    amount = -10.0

    mocker.patch('services.card_service.find_wallet_id', return_value=mock_wallet)
    mocker.patch('services.wallet_service.read_query', return_value=mock_card)
    mocker.patch('services.card_service.read_query', return_value=[(mock_wallet.id, mock_wallet.amount, mock_wallet.user_id)])

    with pytest.raises(HTTPException) as exc_info:
        wallet_service.withdraw_money_from_wallet(user_id, card_id, amount)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Amount must be greater than zero"

def test_get_wallet_balance(mocker, mock_wallet):
    user_id = mock_wallet.user_id

    mocker.patch('services.card_service.find_wallet_id', return_value=mock_wallet)
    mocker.patch('services.card_service.read_query', return_value=[(mock_wallet.id, mock_wallet.amount, mock_wallet.user_id)])

    balance = wallet_service.get_wallet_balance(user_id)

    assert balance == "Current balance = 50.0 leva."


