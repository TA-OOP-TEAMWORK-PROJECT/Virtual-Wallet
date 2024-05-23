from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import Response, HTTPException
import logging

from data_.database import insert_query, update_query, read_query
from data_.models import UserTransfer, User, Transactions, RecurringTransaction, Wallet, TransferConfirmation
from services.card_service import find_wallet_id
from services.user_service import find_by_username, get_user_wallet, find_by_id, get_username_by, add_external_contact, \
    get_contact_list


def user_transfer(cur_transaction: UserTransfer, username: str, cur_user): #В бодито има само сума
 #insert in categories as well !!!!

    receiver_user = find_by_username(username) # да намеря wallet_id i receiver_id

    if not receiver_user:
       return Response(status_code=404, content='There is no user with the given credentials')


    wallet = get_user_wallet(cur_user.id)
    receiver_user_wallet = get_user_wallet(receiver_user.id)


    if wallet.amount < cur_transaction.amount:
        raise HTTPException(status_code=400, detail='Insufficient funds')


    wallet.amount -= cur_transaction.amount
    receiver_user_wallet.amount += cur_transaction.amount

    cur_user_insert = insert_query('''
    INSERT INTO transactions(amount, transaction_date, wallet_id, receiver_id)
    VALUES(?,?,?,?)''',
    (cur_transaction.amount, date.today(), wallet.id, receiver_user.id))

    receiver_user_insert = insert_query('''
    INSERT INTO transactions(amount, transaction_date, wallet_id, receiver_id)
    VALUES(?,?,?,?)''',
    (cur_transaction.amount, date.today(), receiver_user_wallet.id, receiver_user.id))


    cur_user_wallet = update_query('''
    UPDATE wallet
    SET amount = ?
    WHERE user_id = ?''',
   (wallet.amount, cur_user.id))


    receiver_user_wallet = update_query('''
    UPDATE wallet
    SET amount = ?
    WHERE user_id = ?''',
   (receiver_user_wallet.amount, receiver_user.id))

    return Response(status_code=200, content=f'The amount of {cur_transaction.amount} was sent to {receiver_user.username}')


def new_transfer(cur_transaction, search, cur_user):

     receiver = get_username_by(cur_user.id, search, contact_list=False)[1]

     return user_transfer(cur_transaction, receiver, cur_user)


'''
class ExternalContacts(BaseModel):
    id: int | None = None
    is_recurring: int|None = None                     
    recurring_date: date|None = None
    contact_name: str | constr(min_length=2, max_length=100)
    contact_email: EmailStr | None = None
    iban: str | constr(min_length=15, max_length=34)

'''

def bank_transfer(ext_user, cur_transaction, current_user):
    search = ext_user.iban

    def wrapper():
        try:
            external_contact = get_username_by(current_user.id, search, contact_list=True)[1] # da se prekrysti che i tyrsi po neshto w bazata
            contact_list = get_contact_list(current_user, ext_user.contact_name)

            return contact_list


        except HTTPException as ex:
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.error(f"Exception when searching for external contact: {ex}", exc_info=True)

            return  add_external_contact(current_user.id, ext_user)

    contact_list = wrapper()


    wallet = get_user_wallet(current_user.id)


    if wallet.amount < cur_transaction.amount:
        raise HTTPException(status_code=400, detail='Insufficient funds')

    new_wallet_amount: float
    transaction_amount: float
    is_recurring: bool|None = None  #ako ne e recurring
    recurring_date: date|None = None
    recurring_period: int|None = None
    transaction_date: date
    wallet_id: int
    receiver_id: int                   # contact_list_id if is_external is TRue else receiver_id(user in the map)
    is_external:bool

    wallet.amount -= cur_transaction.amount

    transfer_message = TransferConfirmation(new_wallet_amount=wallet.amount,
                                            transaction_amount=cur_transaction.amount,
                                            transaction_date=date.today(),
                                            wallet_id=wallet.id,
                                            receiver_id=contact_list.id,
                                            is_external=True)


    return transfer_message


def process_transfer()




    #
    #
    # cur_user_wallet = update_query('''
    #                   UPDATE wallet
    #                   SET amount = ?
    #                   WHERE user_id = ?''',
    #                   (wallet.amount, current_user.id))
    #
    # if ext_user.is_recurring:
    #     cur_user_insert = insert_query('''
    #                             INSERT INTO transactions(amount, is_recurring, recurring_date, recurring_period, transaction_date, wallet_id, contact_list_id)
    #                             VALUES(?,?,?,?,?,?,?)''',
    #                                    (cur_transaction.amount,  ext_user.is_recurring, ext_user.recurring_date,
    #                                     ext_user.recurring_period, date.today(), wallet.id, contact_list.id))
    #
    # else:
    #
    #     cur_user_insert = insert_query('''
    #                     INSERT INTO transactions(amount, transaction_date, wallet_id, contact_list_id)
    #                     VALUES(?,?,?,?)''',
    #                     (cur_transaction.amount, date.today(), wallet.id, contact_list.id))
    #

def recurring_transactions(): # da izprashtam napravo v bank_transfer?

    today_transactions = read_query('''
    SELECT id, amount, recurring_period, recurring_date, transaction_date, wallet_id, contact_list_id
    FROM transactions
    WHERE is_recurring = 1 
    AND recurring_date = ?''',
    (date.today(), ))



    for transaction in today_transactions:

        cur_transaction = RecurringTransaction.from_query_result(*transaction)
        wallet = get_wallet_by_id(cur_transaction.wallet_id)

        if wallet.amount >= cur_transaction.amount:  #>>>>>>!!!!
            wallet.amount -= cur_transaction.amount


            new_recurring_date = set_new_recurring_date(cur_transaction)

            cur_user_wallet = update_query('''
                                  UPDATE wallet
                                  SET amount = ?
                                  WHERE id = ?''',
                                  (wallet.amount, wallet.id))

            cur_user_insert = insert_query('''
                                INSERT INTO transactions(amount, recurring_date, transaction_date, wallet_id, contact_list_id)
                                VALUES(?,?,?,?,?)''',
                                (cur_transaction.amount, new_recurring_date, date.today(), wallet.id, cur_transaction.contact_list_id))

        else:
            cur_transaction.recurring_date = date.today() + timedelta(days=1)

            update_query('''
            UPDATE transactions
            SET recurring_date = ?
            WHERE id = ?''',
            (cur_transaction.recurring_date, cur_transaction.id))








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

def get_wallet_by_id(wallet_id):

    data = read_query('''
    SELECT id, amount, user_id
    FROM wallet
    WHERE id = ?''',
    (wallet_id, ))

    return Wallet.from_query_result(*data[0])

def set_new_recurring_date(rec_trans):

    new_date = date.today() + timedelta(days=rec_trans.recurring_period)
    return new_date


















# def recurring_transactions():
#
#     today_transactions = read_query('''
#     SELECT id, amount, recurring_period, recurring_date, transaction_date, wallet_id, contact_list_id
#     FROM transactions
#     WHERE is_recurring = 1
#     AND recurring_date = ?''',
#     (date.today(), ))
#
#     for transaction in today_transactions:
#
#         cur_transaction = RecurringTransaction.from_query_result(*transaction)
#         wallet = get_wallet_by_id(cur_transaction.wallet_id)
#
#         if wallet.amount >= cur_transaction.amount:
#             wallet.amount -= cur_transaction.amount
#
#             new_recurring_date = set_new_recurring_date(cur_transaction)
#
#             cur_user_wallet = update_query('''
#                                   UPDATE wallet
#                                   SET amount = ?
#                                   WHERE id = ?''',
#                                   (wallet.amount, wallet.id))
#
#             cur_user_insert = insert_query('''
#                                 INSERT INTO transactions(amount, recurring_date, transaction_date, wallet_id, contact_list_id)
#                                 VALUES(?,?,?,?,?)''',
#                                 (cur_transaction.amount, new_recurring_date, date.today(), wallet.id, cur_transaction.contact_list_id))
#
#         else:
#             raise HTTPException(status_code=400, detail='Insufficient funds to complete the transaction')
