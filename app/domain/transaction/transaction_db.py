import psycopg2
from app.domain.transaction.transaction import Transaction

class TransactionDb:
    @classmethod
    def __init__(cls, db_params):
        cls.db_params = db_params

    @classmethod
    def create_transaction(cls, transaction: Transaction):
        conn = psycopg2.connect(**cls.db_params)
        cur = conn.cursor()

        query = "INSERT INTO accountapi.transactions (transaction_id, account_id, merchant, amount, state, transaction_time) " \
                "VALUES (%s, %s, %s, %s, %s, %s);"
        cur.execute(query, (transaction.transactionId, transaction.accountId, transaction.merchant,
                            transaction.amount, transaction.state, transaction.transactionTime))

        conn.commit()
        cur.close()
        conn.close()

    @classmethod
    def get_transactions(cls):
        conn = psycopg2.connect(**cls.db_params)
        cur = conn.cursor()

        query = "SELECT * FROM accountapi.transactions;"
        cur.execute(query)
        transactions = cur.fetchall()

        cur.close()
        conn.close()
        
        response = [{'transaction_id': item[0], 
                     'account_id': item[1],
                     'merchant': item[2], 
                     'amount': item[3], 
                     'state': item[4], 
                     'transaction_time': item[5]}
                       for item in transactions]

        return response

    @classmethod
    def get_transaction(cls, id):
        conn = psycopg2.connect(**cls.db_params)
        cur = conn.cursor()

        query = "SELECT * FROM accountapi.transactions WHERE transaction_id = %s;"
        cur.execute(query, (id,))
        transaction = cur.fetchone()

        cur.close()
        conn.close()

        if transaction:
            response = {'transaction_id': transaction[0], 
                        'account_id': transaction[1],
                        'merchant': transaction[2], 
                        'amount': transaction[3], 
                        'state': transaction[4], 
                        'transaction_time': transaction[5]}
            return response
        else:
            error_response = {
                "errorCode": 'ToDo',
                "message": f'id {id} não encontrado'
            }
            return error_response
        
    @classmethod
    def get_transactions_by_account_id(cls, id):
        conn = psycopg2.connect(**cls.db_params)
        cur = conn.cursor()

        query = "SELECT * FROM accountapi.transactions WHERE account_id = %s;"
        cur.execute(query, (id,))
        transactions_by_account_id = cur.fetchall()

        cur.close()
        conn.close()

        transactions = []

        for item in transactions_by_account_id:
            transaction_id = item[0]
            merchant = item[2]
            amount = item[3]
            state = item[4]
            transaction_time = item[5]
            
            transaction_data = {
                "transaction_id": transaction_id,
                "merchant": merchant,
                "amount": amount,
                "state": state,
                "transaction_time": transaction_time
            }
            
            transactions.append(transaction_data)

        return transactions
