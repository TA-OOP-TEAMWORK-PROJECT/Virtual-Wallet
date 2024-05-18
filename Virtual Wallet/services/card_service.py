from datetime import datetime

from dateutil.relativedelta import relativedelta
from fastapi import Response
from data_.database import insert_query, read_query, update_query
from data_.models import Wallet


def add(card, user_id, command):

    if is_existing(card.number):
        return Response(status_code=401, content='Card already exists!')

    wallet = find_wallet_id(user_id)

    if command == 'create':
        card.is_virtual = 1
        card.expiration_date = datetime.today().date() + relativedelta(years=5)
    else:
        card.is_virtual = 0

    generated_id = insert_query('''
    INSERT INTO cards(number, exp_date, cardholder_name, cvv, wallet_id, is_virtual)
    VALUES(?,?,?,?,?,?)''',
    (card.number, card.expiration_date,
    card.cardholder_name, card.cvv, wallet.id, card.is_virtual))

    return 'Card was successfully added'


def delete(card_id):

    update_query('''
    DELETE FROM cards  
    WHERE id = ?''',
    (card_id, ))

    return 'Card was successfully deleted!'



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
