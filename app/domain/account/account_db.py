import psycopg2
from app.domain.account.account import Account

class AccountRepository:
    def __init__(self, db_params):
        self.db_params = db_params

    def create_account(self, active_card, available_limit):
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()

        account = Account(active_card, available_limit)
        query = "INSERT INTO accountapi.accounts (accountid, activecard, availablelimit) VALUES (%s, %s, %s);"
        cur.execute(query, (account.account_id, active_card, available_limit))

        conn.commit()
        cur.close()
        conn.close()

        return account

    def get_accounts(self):
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()

        query = "SELECT * FROM accountapi.accounts;"
        cur.execute(query)
        accounts = cur.fetchall()

        cur.close()
        conn.close()

        response = [{'account_id': item[0], 'active_card': item[1], 'available_limit': item[2]} for item in accounts]
        
        return response

    def get_account(self, id):
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()

        query = "SELECT * FROM accountapi.accounts WHERE accountid = %s;"
        cur.execute(query, (id,))
        account = cur.fetchone()

        cur.close()
        conn.close()
        
        if account:
            response = {'account_id': account[0], 'active_card': account[1], 'available_limit': account[2]}
            return response

    def remove_account(self, id):
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()

        query = "DELETE FROM accountapi.accounts WHERE accountid = %s;"
        cur.execute(query, (id,))
        conn.commit()

        rows_affected = cur.rowcount

        cur.close()
        conn.close()

        return rows_affected

    def change_account(self, id, data: dict):
        conn = psycopg2.connect(**self.db_params)
        cur = conn.cursor()

        account = self.get_account(id)
        if account:
            if data.get('active_card') is not None:
                account_change_card_status = data.get('active_card')
                query = "UPDATE accountapi.accounts SET activecard = %s WHERE accountid = %s;"
                cur.execute(query, (account_change_card_status, id))

            if data.get('available_limit') is not None:
                account_update_limit = data.get('available_limit')
                query = "UPDATE accountapi.accounts SET availablelimit = %s WHERE accountid = %s;"
                cur.execute(query, (account_update_limit, id))

            conn.commit()
            cur.close()
            conn.close()

            response = self.get_account(id)

            return response

        error_response = {
            "errorCode": 'ToDo',
            "message": f'id {id} não encontrado'
        }
        return error_response

class AccountDb:
    def __init__(self, db_params):
        self.account_db = AccountRepository(db_params)

    def create_account(self, active_card, available_limit):
        return self.account_db.create_account(active_card, available_limit)

    def get_accounts(self):
        return self.account_db.get_accounts()

    def get_account(self, id):
        return self.account_db.get_account(id)

    def remove_account(self, id):
        return self.account_db.remove_account(id)

    def change_account(self, id, data: dict):
        return self.account_db.change_account(id, data)
    

