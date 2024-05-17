from fastapi import Response
from data_.database import insert_query, read_query
from data_.models import Card


def add(card, user_id):

    c = Card(number=card.number, expiration_date=card.expiration_date,
    cardholder_name=card.cardholder_name, cvv=card.cvv)

    cc = Card.from_query_result(card.number, card.expiration_date,
    card.cardholder_name, card.cvv)

    if is_existing(card.number):
        return Response(status_code=401, content='Card already exists!')

    generated_id = insert_query('''
    INSERT INTO cards(number, exp_date, cardholder_name, cvv, cardholder_id)
    VALUES(?,?,?,?,?)''',
    (card.number, card.expiration_date,
    card.cardholder_name, card.cvv, user_id))

    return 'Card was successfully added'


def is_existing(numb):

    data = read_query('''
    SELECT id 
    FROM cards 
    WHERE number = ?''',
    (numb, ))

    if not data:
        return False
    return True
