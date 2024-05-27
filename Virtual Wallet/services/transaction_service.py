from datetime import date, datetime, timedelta
from typing import Annotated
from fastapi import Response, HTTPException
from data_.database import insert_query, update_query, read_query
from data_.models import UserTransfer, User, Transactions, RecurringTransaction, Wallet, TransferConfirmation
from services.card_service import find_wallet_id
from services.user_service import find_by_username, get_user_wallet, find_by_id, get_contact_external_user
from services.contact_service import get_username_by, add_external_contact, get_contact_list, view_user_contacts

def set_wallet_amount(cur_user, cur_receiver, cur_transaction):
    wallet = get_user_wallet(cur_user.id)

    if wallet.amount < cur_transaction.amount:
        raise HTTPException(status_code=400, detail='Insufficient funds')

    receiver_user_wallet = get_user_wallet(cur_receiver.id)

    wallet.amount -= cur_transaction.amount
    receiver_user_wallet.amount += cur_transaction.amount

    return wallet, receiver_user_wallet
def user_transfer(cur_transaction: UserTransfer, cur_receiver, cur_user, is_in_contacts): #В бодито има само сума #insert in categories as well !!!!


    cur_user_wallet, receiver_wallet = set_wallet_amount(cur_user, cur_receiver, cur_transaction)


    transfer_message = TransferConfirmation(new_wallet_amount=cur_user_wallet.amount,
                                            receiver_wallet_amount=receiver_wallet.amount,
                                            transaction_amount=cur_transaction.amount,
                                            transaction_date=date.today(),
                                            wallet_id=cur_user_wallet.id,
                                            receiver_wallet_id=receiver_wallet.id,
                                            user_id=cur_user.id,
                                            receiver_id=cur_receiver.id,
                                            is_external=False)

    if is_in_contacts:
        return transfer_to_user(transfer_message)

    else:
        return transfer_message

def transfer_to_user(transfer_message): # TODO ako prieme statusa samo se dobavq i t.n.



    cur_user_insert = insert_query('''
    INSERT INTO transactions(amount, transaction_date, wallet_id, receiver_id)
    VALUES(?,?,?,?)''',
    (transfer_message.transaction_amount, date.today(),
                transfer_message.wallet_id, transfer_message.receiver_id))


    user_wallet = update_query('''
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

def in_app_transfer(cur_transaction, search, cur_user): #ук търси в целия апп/ ако искаме директно през контакт лист си имаме @transaction_router.post("/{username}")

    cur_receiver_data = read_query('''
                SELECT id, username, first_name, last_name,
                email, phone_number, role, hashed_password, is_blocked  
                FROM users
                WHERE email LIKE ?
                OR username LIKE ?
                OR phone_number LIKE ?''',
                (f'%{search}%', f'%{search}%', f'%{search}%'))

    if cur_receiver_data is None:
        return Response(status_code=404, content='There is no user with the given credentials')

    cur_receiver = User.from_query_result(*cur_receiver_data[0])
    is_in_contacts = check_contact_list(cur_user.id, cur_receiver.id)

    return user_transfer(cur_transaction, cur_receiver, cur_user, is_in_contacts)


def bank_transfer(ext_user, cur_transaction, current_user):



    contact_list = get_contact_list(current_user, ext_user.contact_name)

    if contact_list is None:

        contact_list = add_external_contact(current_user.id, ext_user)


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


def process_bank_transfer(pending_request): #is_confirmed - в случай, че решим, че искаме да записваме отказани трансфери


    cur_user_wallet = update_query('''
                    UPDATE wallet
                    SET amount = ?
                    WHERE id = ?''',
                    (pending_request.new_wallet_amount, pending_request.wallet_id))


    transaction_insert = insert_query('''
                        INSERT INTO transactions(amount, status, transaction_date, wallet_id, contact_list_id)
                        VALUES(?,?,?,?,?)''',
                        (pending_request.transaction_amount, "confirmed", date.today(),
                                pending_request.wallet_id, pending_request.receiver_id))


       # transaction_id = cur_user_insert
       #  cur_user_update_status = update_query('''
       #  UPDATE transactions
       #  SET status = "confirmed"
       #  WHERE id = ?''',
       #  (cur_user_insert, ))

    # else:
    #
    #     result = transfer_to_user(pending_request)

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




def get_transactions(user: User, search):

    user_wallet = find_wallet_id(user.id)
    data = None

    if search is None:
        data = read_query('''
                   SELECT id, is_recurring, status, amount, transaction_date, receiver_id, contact_list_id, recurring_date
                   FROM transactions
                   WHERE wallet_id = ?
                   OR receiver_id = ?''',
                   (user_wallet.id, user_wallet))

    else:
        try:
            date_format = "%Y-%m-%d"
            search = datetime.strptime(search, date_format)

        except:
            search = find_by_username(search) #

        data = read_query('''
        SELECT id, is_recurring, status, amount, transaction_date, receiver_id, contact_list_id, recurring_date
        FROM transactions
        WHERE wallet_id = ?
        OR receiver_id = ?
        AND (transaction_date LIKE ?
        OR receiver_id LIKE ?)''',
        (user_wallet.id, user_wallet.id, f"%{search}%", f"%{search}%"))


    return [Transactions.get_transactions_query(*t) for t in data]





def sort_transactions(transactions_list, sort_by, is_reverse):

    # transactions_list = [Transactions.from_query_result(i) for i in transactions_list]

    sorted_transactions = None

    if sort_by == 'transaction_date':
        sorted_transactions = sorted(transactions_list, key=lambda x: x.transaction_date, reverse=is_reverse)

    return sorted_transactions

#[Transactions(id=61, is_recurring=False, amount=1.0, status='confirmed', message=None, recurring_period=None, recurring_date=None,
# transaction_date=datetime.date(2024, 5, 27), wallet_id=2, receiver_id=None, contact_list_id=None, category_id=None),
# Transactions(id=63, is_recurring=False, amount=2.0, status='confirmed', message=None, recurring_period=None, recurring_date=None, transaction_date=datetime.date(2024, 5, 27), wallet_id=3, receiver_id=None, contact_list_id=None, category_id=None), Transactions(id=65, is_recurring=False, amount=3.0, status='confirmed', message=None, recurring_period=None, recurring_date=None, transaction_date=datetime.date(2024, 5, 27), wallet_id=3, receiver_id=None, contact_list_id=None, category_id=None), Transactions(id=67, is_recurring=False, amount=555.0, status='confirmed', message=None, recurring_period=None, recurring_date=None, transaction_date=datetime.date(2024, 5, 27), wallet_id=1, receiver_id=None, contact_list_id=None, category_id=None), Transactions(id=68, is_recurring=False, amount=100.0, status='confirmed', message=None, recurring_period=None, recurring_date=None, transaction_date=datetime.date(2024, 5, 27), wallet_id=1, receiver_id=None, contact_list_id=None, category_id=None)]
def get_transaction_response(transactions_list):
    transactions = {}

    for key, value in enumerate(transactions_list):

        # Pyrwo питам дали е рекъринг и си редя json-а и на края питам дали е external и добаваям сенд ту


        if value.is_recurring: # and value.contact_list_id:


            transactions[key + 1] = {
                "Reccuring": 'Transaction is recurring',
                "Amount": value.amount,
                "Status": value.status,
                "Date of next transfer": value.recurring_date,
                "Last transfer date": value.transaction_date,

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
            external_receiver = get_contact_external_user(value.contact_list_id)
            transactions[key + 1]["Send to"] = f"{external_receiver.contact_name}"

    return transactions


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


def get_transaction_by_id(id:int ):

    data = read_query('''
    SELECT id, is_recurring, status, amount, transaction_date, receiver_id, contact_list_id, recurring_date
    FROM transactions
    WHERE id = ?''',
    (id, ))

    return Transactions.get_transactions_query(*data[0])

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
def process_to_user_approval(request):

    data = insert_query('''
    INSERT INTO transactions(amount, transaction_date, wallet_id, receiver_id)
    VALUES(?,?,?,?)''',
    (request.transaction_amount, request.transaction_date, request.wallet_id, request.receiver_id))


def change_status(id, new_status, cur_user):  # trqbva li proverka za tova dali ima takava tranzakciq i za user-a//

    transaction = get_transaction_by_id(id)

    if transaction.status == new_status:
        return Response(status_code=400, content='Not supported operation')


    update_query('''
        UPDATE transactions
        SET status = ?
        WHERE id = ?''',
        (new_status, id))

    if new_status == 'denied':
        return Response(status_code=200, content='You denied the transaction')


    cur_receiver = find_by_id(transaction.receiver_id)
    cur_user_wallet, receiver_wallet = set_wallet_amount(cur_user, cur_receiver,
                                                         UserTransfer(amount=transaction.amount))

    user_wallet = update_query('''
            UPDATE wallet
            SET amount = ?
            WHERE user_id = ?''',
            (cur_user_wallet.amount, cur_user.id))

    receiver_user_wallet = update_query('''
            UPDATE wallet
            SET amount = ?
            WHERE user_id = ?''',
            (receiver_wallet.amount, cur_receiver.id))

    insert_query('''
    INSERT INTO contact_list(user_id, contact_id)  
    VALUES(?,?)''',
    (cur_user.id, transaction.receiver_id))

    return 'The transaction was approved'



def app_recurring_transaction(app_rec_transaction: Transactions, cur_user):

    user_wallet = get_user_wallet(cur_user.id)
    insert_query('''
    INSERT INTO transactions(is_recurring, amount, recurring_period, 
    recurring_date, transaction_date, wallet_id, receiver_id)
    VALUES(?,?,?,?,?,?,?)''',
                 (1, app_rec_transaction.amount, app_rec_transaction.recurring_period,
                  app_rec_transaction.recurring_date, app_rec_transaction.transaction_date,
                  user_wallet.id, app_rec_transaction.receiver_id))

    transaction_list = [app_rec_transaction]

    return get_transaction_response(transaction_list)


def external_recurring_transaction(ext_rec_transaction: Transactions, cur_user):

    user_wallet = get_user_wallet(cur_user.id)
    insert_query('''
    INSERT INTO transactions(is_recurring, amount, recurring_period, 
    recurring_date, transaction_date, wallet_id, contact_list_id)
    VALUES(?,?,?,?,?,?,?)''',
                 (1, ext_rec_transaction.amount, ext_rec_transaction.recurring_period,
                  ext_rec_transaction.recurring_date, ext_rec_transaction.transaction_date,
                  user_wallet.id, ext_rec_transaction.contact_list_id))

    transaction_list = [ext_rec_transaction]

    return get_transaction_response(transaction_list)





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
