import unittest
import psycopg2
from app import create_app
from app.domain.transaction.transaction_db import TransactionDb
from app.domain.account.account_db import AccountDb
from app.domain.account.account import Account
from app.domain.transaction.transaction import Transaction

class TransactionControllerTestCase(unittest.TestCase):

    def setUp(self):
        db_params = {
            "dbname": "test_infnet",
            "user": "postgres",
            "password": "aquelasenha",
            "host": "192.168.0.14",
            "port": "5433"
        }
        self.app = create_app(db_params)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.transaction_db = TransactionDb(db_params)
        self.account_db = AccountDb(db_params)

    def tearDown(self):
        conn = psycopg2.connect(**self.app.config['DB_PARAMS'])
        cur = conn.cursor()

        cur.execute("DELETE FROM accountapi.transactions;")

        conn.commit()
        cur.close()
        conn.close()


    def test_create_transaction_success(self):
        account = self.account_db.create_account(True, 2000)
        account_id = account.account_id
        self.transaction_db.create_transaction = lambda self, transaction: None

        transaction_data = {
            "account_id": account_id,
            "merchant": "Example Merchant",
            "amount": 100.0
        }

        response = self.client.post('/api/transaction/', json=transaction_data)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "success")

    def test_create_transaction_card_inactive(self):
        account = self.account_db.create_account(False, 2000)
        account_id = account.account_id

        transaction_data = {
            "account_id": account_id,
            "merchant": "Example Merchant",
            "amount": 100.0
        }

        response = self.client.post('/api/transaction/', json=transaction_data)

        self.assertEqual(response.status_code, 403)
        data = response.get_json()
        self.assertEqual(data["message"], "Card not active")

    def test_create_transaction_insufficient_balance(self):
        account = self.account_db.create_account(True, 100)
        account_id = account.account_id

        transaction_data = {
            "account_id": account_id,
            "merchant": "Example Merchant",
            "amount": 200.0
        }

        response = self.client.post('/api/transaction/', json=transaction_data)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["message"], "Insufficient limit")

    def test_create_transaction_high_frequency(self):
        account = self.account_db.create_account(True, 20000)
        account_id = account.account_id
        self.transaction_db.get_transactions_by_account_id = lambda self, id: [
            Transaction("Merchant", 100.0, "Success", account_id)
            for _ in range(4)
        ]
        
        for i in range(4):
            transaction_data = {
                "account_id": account_id,
                "merchant": "Example Merchant",
                "amount": 150.0*i
            }

            response = self.client.post('/api/transaction/', json=transaction_data)

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["message"], "High frequency small interval")

if __name__ == '__main__':
    unittest.main()
