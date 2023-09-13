import unittest
import psycopg2
from app import create_app
from app.domain.account.account_db import AccountDb

class AccountControllerTestCase(unittest.TestCase):

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
        self.account_db = AccountDb(db_params)

    def tearDown(self):
        conn = psycopg2.connect(**self.app.config['DB_PARAMS'])
        cur = conn.cursor()

        cur.execute("DELETE FROM accountapi.accounts;")

        conn.commit()
        cur.close()
        conn.close()

    def test_get_accounts(self):
        self.account_db.create_account(True, 1000)
        self.account_db.create_account(False, 500)

        response = self.client.get('/api/account/')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

    def test_create_account(self):
        account_data = {
            "active_card": True,
            "available_limit": 1500
        }

        response = self.client.post('/api/account/', json=account_data)

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("account", data)
        account = data["account"]
        self.assertTrue(account["active_card"])
        self.assertEqual(account["available_limit"], 1500)

    def test_get_account_by_id(self):
        account = self.account_db.create_account(True, 2000)
        account_id = account.account_id

        self.account_db.get_account = lambda id: account if id == account_id else None

        response = self.client.get(f'/api/account/{account_id}')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["active_card"], True)
        self.assertEqual(data["available_limit"], 2000)

    def test_get_account_by_invalid_id(self):
        response = self.client.get('/api/account/999')

        self.assertEqual(response.status_code, 404)

    def test_update_account(self):
        account = self.account_db.create_account(True, 2000)
        account_id = account.account_id
        updated_data = {
            "active_card": False,
            "available_limit": 1200
        }
        self.account_db.change_account = lambda id, data: data if id == account_id else None

        response = self.client.put(f'/api/account/{account_id}', json=updated_data)

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["active_card"], False)
        self.assertEqual(data["available_limit"], 1200)

    def test_delete_account(self):
        account = self.account_db.create_account(False, 2000)
        account_id = account.account_id
        self.account_db.remove_account = lambda id: 204 if id == account_id else 404

        response = self.client.delete(f'/api/account/{account_id}')

        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_account(self):
        response = self.client.delete('/api/account/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
