from datetime import date, datetime
from fastapi import Response, HTTPException
import logging
from data_.database import insert_query, update_query, read_query
from data_.models import UserTransfer, User, Transactions
from services.card_service import find_wallet_id
from services.user_service import find_by_username, get_user_wallet, find_by_id, get_username_by, add_external_contact


def user_transfer(cur_transaction: UserTransfer, username: str, cur_user): #В бодито има само сума
 #insert in categories as well !!!!

    receiver_user = find_by_username(username) # да намеря wallet_id i receiver_id

    if not receiver_user:
       return Response(status_code=404, content='There is no user with the given credentials')


    cur_user_wallet = get_user_wallet(cur_user.id)
    receiver_user_wallet = get_user_wallet(receiver_user.id)   # da proverq dali ima dostatychno v walleta

    cur_user_insert = insert_query('''
    INSERT INTO transactions(amount, transaction_date, wallet_id, receiver_id)
    VALUES(?,?,?,?)''',
    (cur_transaction.amount, date.today(), cur_user_wallet.id, receiver_user.id))

    receiver_user_insert = insert_query('''
    INSERT INTO transactions(amount, transaction_date, wallet_id, receiver_id)
    VALUES(?,?,?,?)''',
    (cur_transaction.amount, date.today(), receiver_user_wallet.id, receiver_user.id))

    cur_user_wallet.amount -= cur_transaction.amount
    receiver_user_wallet.amount += cur_transaction.amount

    cur_user_wallet = update_query('''
    UPDATE wallet
    SET amount = ?
    WHERE user_id = ?''',
   (cur_user_wallet.amount, cur_user.id))


    receiver_user_wallet = update_query('''
    UPDATE wallet
    SET amount = ?
    WHERE user_id = ?''',
   (receiver_user_wallet.amount, receiver_user.id))

    return Response(status_code=200, content=f'The amount of {cur_transaction.amount} was sent to {receiver_user.username}')


def new_transfer(cur_transaction, search, cur_user):

     receiver = get_username_by(cur_user.id, search, contact_list=False)[1]

     return user_transfer(cur_transaction, receiver, cur_user)


def bank_transfer(ext_user, cur_transaction, current_user):
    search = ext_user.iban

    def wrapper():
        try:
            external_contact = get_username_by(ext_user, search, contact_list=True)[1]
            return external_contact # napishi si func deto namira po iban extusers
        except HTTPException as ex:
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.error(f"Exception when searching for external contact: {ex}", exc_info=True)

            add_external_contact(current_user.id, ext_user)

    wrapper()









def get_transactions(user: User, search):  # ako e nevaliden search

    user_wallet = find_wallet_id(user.id)
    data = None

    if search is None:
        data = read_query('''
           SELECT id, is_recurring, amount, status, message, transaction_date, recurring_date, wallet_id, receiver_id
           FROM transactions
           WHERE wallet_id = ?''',
           (user_wallet.id,))


    else:
        try:
            date_format = "%Y-%m-%d"
            datetime.strptime(search, date_format)


            data = read_query('''
            SELECT id, is_recurring, amount, status, message, transaction_date, recurring_date, wallet_id, receiver_id
            FROM transactions
            WHERE wallet_id = ? 
            AND transaction_date = ?''',
            (user_wallet.id, search))

        except:


            receiver = find_by_username(search)

            data = read_query('''
            SELECT id, is_recurring, amount, status, message, transaction_date, recurring_date, wallet_id, receiver_id
            FROM transactions
            WHERE wallet_id = ? 
            AND receiver_id = ?''',
            (user_wallet.id, receiver.id))


    return data


def sort_transactions(transactions_list, sort_by, is_reverse):

    # transactions_list = [Transactions.from_query_result(i) for i in transactions_list]
    updated_transaction_list = []
    for data in transactions_list:

        id, is_recurring, amount, status, message, transaction_date, recurring_date, wallet_id, receiver_id = data

        updated_transaction_list.append(Transactions.from_query_result
                                        (id, is_recurring, amount, status,
                                         message, transaction_date, recurring_date,
                                         wallet_id, receiver_id))

    sorted_transactions = None
    if not sort_by:
        sorted_transactions = sorted(updated_transaction_list, reverse=is_reverse)

    if sort_by == 'transaction_date':
        sorted_transactions = sorted(updated_transaction_list, key=lambda x: x.transaction_date, reverse=is_reverse)

    return sorted_transactions

def get_transaction_response(transactions_list):

    transactions = {}

    for key,value in enumerate(transactions_list):


        receiver = find_by_id(value.receiver_id)

        if value.is_recurring:

            transactions[key + 1] = {
                 "Reccuring": 'Transaction is recurring',
                 "Amount": value.amount,
                 "Status": value.status,
                 "Date of next transfer": value.recurring_date,
                 "Last transfer date": value.transaction_date,
                 "Send to": f"{receiver.first_name} {receiver.last_name}"
            }

        else:

            transactions[key + 1] = {
                "Amount": value.amount,
                "Status": value.status,
                "Date of next transfer": value.recurring_date,
                "Last transfer date": value.transaction_date,
                "Send to": f"{receiver.first_name} {receiver.last_name}"
            }

    return transactions


def change_status(id, new_status): #trqbva li proverka za tova dali ima takava tranzakciq i za user-a// zaz tova dali e validna proverkata

    transaction = get_transaction_by_id(id)

    if not transaction.status == new_status:

        update_query('''
        UPDATE transactions
        SET status = ?
        WHERE id = ?''',
        (new_status, id))

        if new_status == 'denied':
            return Response(status_code=200, content='You denied the transaction')
        return Response(status_code=200, content='You confirmed the transaction')

    else:
        return Response(status_code=400, content='Not supported operation')



def get_transaction_by_id(id):

    data = read_query('''
    SELECT id, is_recurring, amount, status, message, transaction_date, recurring_date, wallet_id, receiver_id
    FROM transactions
    WHERE id = ?''',
    (id, ))

    # id, is_recurring, amount, status, message, transaction_date, recurring_date, wallet_id, receiver_id = data[0]

    return Transactions.from_query_result(*data[0])

