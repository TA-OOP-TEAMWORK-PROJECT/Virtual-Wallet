import datetime
from datetime import datetime

from data_.models import Transactions

transactions = [
                {'id': 1,'is_recurring': 1, 'amount': 100, 'status': 'confirmed', 'message':'Hi', 'recurring_period': 10, 'recurring_date': datetime.strptime('2025-06-12', "%Y-%m-%d"),
                 'transaction_date': datetime.strptime('2024-06-12', "%Y-%m-%d"), 'wallet_id': 1, 'receiver_id': 1, 'contact_list_id': 1, 'category_id': 4},
                {'id': 2, 'is_recurring': 0, 'amount': 200, 'status': 'pending','message':'How r u', 'recurring_period': 20, 'recurring_date': None,
                 'transaction_date': datetime.strptime('2024-07-12', "%Y-%m-%d"),'wallet_id': 2, 'receiver_id': 2, 'contact_list_id': None, 'category_id': 3},
                {'id': 3, 'is_recurring': 0, 'amount': 300, 'status': 'confirmed', 'message':'Za semki', 'recurring_period': 30, 'recurring_date': None,
                 'transaction_date': datetime.strptime('2023-06-12', "%Y-%m-%d"), 'wallet_id': 3, 'receiver_id': None, 'contact_list_id': 2, 'category_id': 2},
                {'id': 4, 'is_recurring': 0, 'amount': 400, 'status': 'denied', 'message':'To have','recurring_period': 40, 'recurring_date': None,
                 'transaction_date': datetime.strptime('2022-06-12', "%Y-%m-%d"), 'wallet_id': 4, 'receiver_id': 5, 'contact_list_id': None, 'category_id': 1}
                ]


transactions_class = [Transactions.from_query_result(*t.values()) for t in transactions]

users = [
    {'id': 1, 'username': 'ikonata', 'first_name': 'Valeri', 'last_name': 'Bojinov', 'email': 'user@example.com', 'phone_number': '0899562314',
     'hashed_password': '$12$t6.YYwDAFyf/9WAa8I7/xuCr40I42RviZdd3hR7.Z1nRLPTzxT5wC', 'is_blocked': 0, 'role': 0}
]


def get_transaction_response(transactions_list):
    transactions = {}

    for key, value in enumerate(transactions_list):

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
            transactions[key + 1]["Send to"] = f"Valeri Bojinov"

        else:
            external_receiver = 1
            if external_receiver:
                transactions[key + 1]["Send to"] = f"Valeri Bojinov"
            else:
                transactions[key + 1]["Send to"] = "Removed external contact"

    return transactions