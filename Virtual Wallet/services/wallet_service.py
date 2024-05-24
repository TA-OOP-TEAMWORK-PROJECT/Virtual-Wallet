from datetime import datetime

from dateutil.relativedelta import relativedelta
from fastapi import Response, HTTPException
from data_.database import insert_query, read_query, update_query
from data_.models import Wallet
from services.user_service import find_by_id


def add(card, user_id, command):

    if is_existing(card.number):
        return Response(status_code=401, content='Card already exists!')

    wallet = find_wallet_id(user_id)
    user = find_by_id(user_id)

    if command == 'create':
        card.is_virtual = 1
        card.expiration_date = datetime.today().date() + relativedelta(years=5)
    else:
        card.is_virtual = 0

    card.cardholder_name = f"{user.first_name} {user.last_name}"

    generated_id = insert_query('''
    INSERT INTO cards(number, exp_date, cardholder_name, cvv, wallet_id, is_virtual)
    VALUES(?,?,?,?,?,?)''',
    (card.number, card.expiration_date,
    card.cardholder_name, card.cvv, wallet.id, card.is_virtual))

    card_type = type_card(card.number)
    return f'Your {card_type} card was successfully added'


def delete(card_id: int, user_id: int) -> str:
    card_data = read_query('''
        SELECT id 
        FROM cards 
        WHERE id = ? AND wallet_id = (SELECT id FROM wallet WHERE user_id = ?)
    ''', (card_id, user_id))

    if not card_data:
        raise HTTPException(status_code=404, detail="Card not found or does not belong to the user.")

    update_query('''
        DELETE FROM cards  
        WHERE id = ?''',
        (card_id,))

    return 'Your Card was successfully deleted!'



def find_wallet_id(user_id):

     data = read_query('''
        SELECT id, amount, user_id
        FROM wallet
        WHERE user_id = ?''',
        (user_id,))

     id, amount, user_id = data[0]

     return Wallet(id=id, amount=amount, user_id=user_id)


def is_existing(numb):

    data = read_query('''
    SELECT id 
    FROM cards 
    WHERE number = ?''',
    (numb, ))

    if not data:
        return False
    return True

def type_card(number):

    if number.startswith("4"):
        return 'VISA'

    if (51 <= int(number[:2]) <= 55) or 2221 <= int(number[:2]) <= 2720:
        return 'MASTER'

    return ''


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




