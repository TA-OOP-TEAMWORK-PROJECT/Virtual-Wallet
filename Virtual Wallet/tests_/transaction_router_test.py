import unittest
from datetime import datetime, date
from unittest.mock import MagicMock, patch

from tests_.mock_transactions_data import transactions, transactions_class, get_transaction_response
from data_.models import User
from routers import transaction_router
from fastapi.testclient import TestClient
from main import app



class TransactionRouter(unittest.TestCase):


    def setUp(self):
        test_current_user = User(id=1, username='ikonata', password=None, first_name='Valeri',
                        last_name='Bojinov', email='user@example.com', phone_number='0888556677',  role='user', hashed_password='$2b$12$t6.YYwDAFyf/9WAa8I7/xuCr40I42RviZdd3hR7.Z1nRLPTzxT5wC')

        self.client = TestClient(app)
        self.mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnb3NobzEyMyIsImV4cCI6MTcxNzk2Mzc0N30.PsV3qMBsufM36CWjBRODQxSWPgVPIN2MCQNjheLIkqY"

    @patch('routers.transaction_router.get_transactions') #
    def test_view_transactions(self, mock_get_transactions):

        mock_get_transactions.return_value = transactions_class

        with patch('routers.transaction_router.get_transaction_response'):
            response = {
                "Reccuring": "Transaction is recurring",
                "Amount": 100.0,
                "Status": 'confirmed',
                "Date of next transfer": date(2025, 6, 12),
                "Last transfer date": date(2024, 6, 12),
                "Send to": "Valeri Bojinov"
            }

            self.assertEqual(response, get_transaction_response(mock_get_transactions.return_value)[1])

        # headers = {"Authorization": f"Bearer {self.mock_token}"}
        # response = self.client.get("/transactions/", headers=headers)



        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.json(), transactions)

    # @patch('routers.transactions.get_transactions')
    # def test_read_transactions(self, mock_get_transactions):
    #     # Set the mock object to return mock data

    @patch('routers.transaction_router.view_all_recuring_transactions')
    def  test_view_recurring_transaction(self, mock_all_recuring_transactions):
        mock_all_recuring_transactions.return_value = transactions[0]





    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()


