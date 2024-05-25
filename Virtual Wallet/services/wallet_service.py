from fastapi import Response, HTTPException
from data_.database import insert_query, read_query, update_query
from services.card_service import find_wallet_id


def add_money_to_wallet(user_id: int, card_id: int, amount: float):
    wallet = find_wallet_id(user_id)

    card = read_query('''
        SELECT id FROM cards WHERE id = ? AND wallet_id = ?
    ''', (card_id, wallet.id))

    if not card:
        raise HTTPException(status_code=404, detail="Card not found or does not belong to user")

    new_amount = wallet.amount + amount
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    update_query('''
        UPDATE wallet SET amount = ? WHERE id = ?
    ''', (new_amount, wallet.id))

    return f"{amount} leva were successfully added to your wallet. Current balance = {new_amount} leva."


def withdraw_money_from_wallet(user_id: int, card_id: int, amount: float):
    wallet = find_wallet_id(user_id)

    if wallet.amount < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds in wallet")

    card = read_query('''
        SELECT id FROM cards WHERE id = ? AND wallet_id = ?
    ''', (card_id, wallet.id))

    if not card:
        raise HTTPException(status_code=404, detail="Card not found or does not belong to user")

    new_amount = wallet.amount - amount
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    update_query('''
        UPDATE wallet SET amount = ? WHERE id = ?
    ''', (new_amount, wallet.id))

    return f"{amount} leva were successfully withdrawn from your wallet. Current balance = {new_amount} leva."


def get_wallet_balance(user_id: int) -> float:
    wallet = find_wallet_id(user_id)
    return f"Current balance = {wallet.amount} leva."