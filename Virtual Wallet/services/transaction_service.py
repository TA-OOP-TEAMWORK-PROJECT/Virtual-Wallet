from datetime import date, datetime, timedelta
from typing import Annotated
from fastapi import Response, HTTPException
from data_.database import insert_query, update_query, read_query
from data_.models import UserTransfer, User, Transactions, RecurringTransaction, Wallet, TransferConfirmation
from services.card_service import find_wallet_id
from services.user_service import find_by_username, get_user_wallet, find_by_id
from services.contact_service import get_username_by, add_external_contact, get_contact_list, view_user_contacts


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

    is_friend = check_contact_list(cur_user.id, receiver_user.id)

#transaction_id v transfer_message
    transfer_message = TransferConfirmation(new_wallet_amount=wallet.amount,
                                            receiver_wallet_amount=receiver_user_wallet.amount,
                                            transaction_amount=cur_transaction.amount,
                                            transaction_date=date.today(),
                                            wallet_id=wallet.id,
                                            receiver_wallet_id=receiver_user_wallet.id,
                                            user_id=cur_user.id,
                                            receiver_id=receiver_user.id,
                                            is_external=False)

    if is_friend:
        return transfer_to_user(transfer_message)



    else:

        return transfer_message

def transfer_to_user(transfer_message):


    cur_user_insert = insert_query('''
    INSERT INTO transactions(amount, transaction_date, wallet_id, receiver_id)
    VALUES(?,?,?,?)''',
    (transfer_message.transaction_amount, date.today(),
                transfer_message.wallet_id, transfer_message.receiver_id))

    receiver_user_insert = insert_query('''
    INSERT INTO transactions(amount, transaction_date, wallet_id, receiver_id)
    VALUES(?,?,?,?)''',
    (transfer_message.transaction_amount, date.today(),
                transfer_message.receiver_wallet_id, transfer_message.receiver_id))


    cur_user_wallet = update_query('''
    UPDATE wallet
    SET amount = ?
    WHERE user_id = ?''',
   (transfer_message.new_wallet_amount, transfer_message.user_id))


    receiver_user_wallet = update_query('''
    UPDATE wallet
    SET amount = ?
    WHERE user_id = ?''',
   (transfer_message.receiver_wallet_amount, transfer_message.receiver_id))

    id_user_transaction = cur_user_insert
    status_update_cur_user = update_query('''
    UPDATE transactions
    SET status = "confirmed"
    WHERE id = ?''',
     (id_user_transaction, ))

    id_receiver = receiver_user_insert
    status_update_cur_user = update_query('''
    UPDATE transactions
    SET status = "confirmed"
    WHERE id = ?''',
     (id_receiver, ))

    raise HTTPException(status_code=200, detail=f'The amount of {transfer_message.transaction_amount} was sent.')

def check_contact_list(sender_id, receiver_id):

    data = read_query('''
    SELECT CASE 
    WHEN EXISTS (SELECT 1 FROM contact_list 
    WHERE contact_id = ? AND user_id = ?)
	THEN TRUE 
    ELSE FALSE 
    END AS result''',
    (sender_id, receiver_id))

    if data[0][0] == 1:
        return True
    return False

def new_transfer(cur_transaction, search, cur_user): #ук търси в целия апп/ ако искаме директно през контакт лист си имаме @transaction_router.post("/{username}")

     receiver_username = get_username_by(cur_user.id, search, contact_list=False)[1]

     return user_transfer(cur_transaction, receiver_username, cur_user)


def bank_transfer(ext_user, cur_transaction, current_user):
    search = ext_user.iban

    def wrapper():
        try:
            external_contact = get_username_by(current_user.id, search, contact_list=True, is_external=True)[1] # da se prekrysti che i tyrsi po neshto w bazata
            contact_list = get_contact_list(current_user, ext_user.contact_name)

            return contact_list


        except HTTPException as ex:


            return  add_external_contact(current_user.id, ext_user)

    contact_list = wrapper()


    wallet = get_user_wallet(current_user.id)


    if wallet.amount < cur_transaction.amount:
        raise HTTPException(status_code=400, detail='Insufficient funds')


    wallet.amount -= cur_transaction.amount

    transfer_message = TransferConfirmation(new_wallet_amount=wallet.amount,
                                            transaction_amount=cur_transaction.amount,
                                            transaction_date=date.today(),
                                            wallet_id=wallet.id,
                                            receiver_id=contact_list.id,
                                            is_external=True)


    return transfer_message


def process_transfer(pending_request): #is_confirmed - в случай, че решим, че искаме да записваме отказани трансфери



    if pending_request.is_external:
        cur_user_wallet = update_query('''
                              UPDATE wallet
                              SET amount = ?
                              WHERE id = ?''',
                                       (pending_request.new_wallet_amount, pending_request.wallet_id))


        cur_user_insert = insert_query('''
                                INSERT INTO transactions(amount, transaction_date, wallet_id, contact_list_id)
                                VALUES(?,?,?,?)''',
                                           (pending_request.transaction_amount, date.today(),
                                            pending_request.wallet_id, pending_request.receiver_id))

        transaction_id = cur_user_insert
        cur_user_update_status = update_query('''
        UPDATE transactions
        SET status = "confirmed"
        WHERE id = ?''',
        (cur_user_insert, ))

    else:

        result = transfer_to_user(pending_request)

def get_recuring_transactions(search_by, search): #search e data, ako tyrsim vsichki tranzakcii ili user_id ako samo na 1 user

    if search_by == 'Date':

        today_transactions = read_query('''
              SELECT id, amount, recurring_period, recurring_date, transaction_date, wallet_id, contact_list_id
              FROM transactions
              WHERE is_recurring = 1 
              AND recurring_date = ?''',
             (search, ))

        return today_transactions

    if search_by == "User":

        wallet_id = get_user_wallet(search.id) #is_recurring

        transactions = read_query('''
          SELECT id, is_recurring, amount, recurring_period, recurring_date, transaction_date, wallet_id, contact_list_id
          FROM transactions
          WHERE is_recurring = 1
          AND wallet_id = 1 ''',
          (wallet_id, ))

        if transactions is None:
            pass

    transactions_result = [Transactions.create_transaction_class(*t) for t in transactions]
    return get_transaction_response(transactions_result) #TODO - da izliza kat' orata



def recurring_transactions():

    today_transactions = get_recuring_transactions("Date", date.today())

    #     read_query('''
    # SELECT id, amount, recurring_period, recurring_date, transaction_date, wallet_id, contact_list_id
    # FROM transactions
    # WHERE is_recurring = 1
    # AND recurring_date = ?''',
    # (date.today(), ))

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
           SELECT id, is_recurring, amount, message, recurring_date, transaction_date, wallet_id, receiver_id, contact_list_id
           FROM transactions
           WHERE wallet_id = ?''',
           (user_wallet.id, ))


    else:
        try:
            date_format = "%Y-%m-%d"
            datetime.strptime(search, date_format)


            data = read_query('''
            SELECT id, is_recurring, amount, message, recurring_date, transaction_date, wallet_id, receiver_id, contact_list_id
            FROM transactions
            WHERE wallet_id = ? 
            AND transaction_date = ?''',
            (user_wallet.id, search))

        except:


            receiver = find_by_username(search)

            data = read_query('''
            SELECT id, is_recurring, amount, message, recurring_date, transaction_date, wallet_id, receiver_id, contact_list_id
            FROM transactions
            WHERE wallet_id = ? 
            AND receiver_id = ?''',
            (user_wallet.id, receiver.id))


    return [Transactions.create_transaction_class(*t) for t in data]


def sort_transactions(transactions_list, sort_by, is_reverse):

    # transactions_list = [Transactions.from_query_result(i) for i in transactions_list]
    updated_transaction_list = []
    for data in transactions_list:

        id, is_recurring, amount, status, message, transaction_date, recurring_date, wallet_id, receiver_id, contact_list_id = data

        updated_transaction_list.append(Transactions.from_query_result
                                        (id, is_recurring, amount, status,
                                         message, transaction_date, recurring_date,
                                         wallet_id, receiver_id, contact_list_id))

    sorted_transactions = None
    if not sort_by:
        sorted_transactions = sorted(updated_transaction_list, reverse=is_reverse)

    if sort_by == 'transaction_date':
        sorted_transactions = sorted(updated_transaction_list, key=lambda x: x.transaction_date, reverse=is_reverse)

    return sorted_transactions

def get_transaction_response(transactions_list):
    transactions = {}

    for key, value in enumerate(transactions_list):

        # Pyrwo питам дали е рекъринг и си редя json-а и на края питам дали е external и добаваям сенд ту


        if value.is_recurring:
            transactions[key + 1] = {
                "Reccuring": 'Transaction is recurring',
                "Amount": value.amount,
                "Status": value.status,
                "Date of next transfer": value.recurring_date,
                "Last transfer date": value.transaction_date
            }

        if not value.is_recurring:
            transactions[key + 1] = {
                "Amount": value.amount,
                "Status": value.status,
                "Date of next transfer": value.recurring_date,
                "Last transfer date": value.transaction_date
            }

        if value.receiver_id:
            receiver = find_by_id(value.receiver_id)
            transactions[key + 1]["Send to"] = f"{receiver.first_name} {receiver.last_name}"

        else:
            external_receiver = find_external_user_contact_list(value.contact_list_id)
            transactions[key + 1]["Send to"] = f"{external_receiver.contact_name}"


def find_external_user_contact_list(contact_list_id: int):

    external_user_id_data = read_query(
        '''SELECT external_user_id
                  FROM contact_list
                  WHERE id = ?''',
        (contact_list_id, ))[0][0]

    external_user_data = read_query('''
    SELECT id, contact_name, contact_email, iban
    FROM external_user 
    WHERE id =?''',
    (external_user_id_data, ))

    return next((User.from_query_result(*row) for row in external_user_data), None) # TODO GYRMIIIII TUUK




def change_status(id, new_status): #trqbva li proverka za tova dali ima takava tranzakciq i za user-a// zaz tova dali e validna proverkata

    transaction = get_transaction_by_id(id)

    if not transaction.status == new_status:

        update_query('''
        UPDATE transactions
        SET status = ?
        WHERE id = ?''',
        (new_status, id))

        if new_status == 'denied': # да сменя статуса за двамата в базата
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


def confirmation_respose(pending_transaction, name):

    return {
        "Amount to pay":pending_transaction.transaction_amount,
        "Date of payment": date.today(),
        "Receiver": name
    }
    # new_wallet_amount = wallet.amount,
    # transaction_amount = cur_transaction.amount,
    # transaction_date = date.today(),
    # wallet_id = wallet.id,
    # receiver_id = contact_list.id,
    # is_external = True)














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
