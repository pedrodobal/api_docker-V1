from flask_restplus import Resource, Namespace, fields
from flask import request, current_app
from app.domain.transaction.transaction_db import TransactionDb
from app.domain.account.account_db import AccountDb
from app.domain.merchant.merchant import Merchant
from app.domain.transaction.transaction import Transaction
from app.domain.account.account import Account

TRANSACTION_INTERVAL = 120

api = Namespace('Transaction', description='Transaction Manager')
model = api.model('TransactionModel', {
    'accountId': fields.String,
    'merchant': fields.String,
    'amount': fields.Float
})

@api.route('/')
class TransactionController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transaction_db = TransactionDb(current_app.config.get('DB_PARAMS'))
        self.account_db = AccountDb(current_app.config.get('DB_PARAMS'))

    @api.response(200, "Found with success")
    def get(self):
        response = self.transaction_db.get_transactions()
        return response, 200 
    
    @api.expect(model)
    @api.param('accountId','account id',)
    @api.param('merchant','merchant name')
    @api.param('amount','value amount')
    def post(self):
        data = request.get_json()
        
        required_fields = ['accountId', 'merchant', 'amount']
        if not all(field in data for field in required_fields):
            response = {
                "message": 'bad request'
            }
            return response, 400

        account_id = data["accountId"]
        account = self.account_db.get_account(account_id)
        
        if account:
            merchant = Merchant(data["merchant"])
            account = Account(account['activecard'], account['availablelimit'], account_id)
            transaction = Transaction(merchant.merchantName, data["amount"], "Processing", account.accountId)
            
            if not account.isCardActive():
                response = {
                    "message": 'Card not active'
                }
                transaction.state = "Card Blocked"
                self.transaction_db.create_transaction(transaction)
                return response, 403
            
            if not account.checkLimit(transaction.amount):
                response = {
                    "message": 'Insufficient limit'
                }
                transaction.state = "Insufficient Balance"
                self.transaction_db.create_transaction(transaction)
                return response, 400
            
            account_transactions = account.getTransactions()
            interval_start = transaction.transactionTime - TRANSACTION_INTERVAL

            account_recent_transactions = [
                account_transaction
                for account_transaction in account_transactions
                if account_transaction['transaction_time'] > interval_start
            ]

            if len(account_recent_transactions) >= 3:
                response = {
                    "message": 'High frequency small interval'
                }
                transaction.state = "High Frequency Small Interval"
                self.transaction_db.create_transaction(transaction)
                return response, 400
            
            duplicate_transactions = [t for t in account_recent_transactions if t['amount'] == transaction.amount and t['merchant'] == merchant.merchantName]
            
            if len(duplicate_transactions) >= 1:
                response = {
                    "message": 'Doubled transaction'
                }
                transaction.state = "Doubled Transaction"
                self.transaction_db.create_transaction(transaction)
                return response, 400
            
            new_limit = account.availableLimit - transaction.amount
            account.updateLimit(new_limit)
            self.account_db.change_account(account.accountId, account.__dict__)
            
            response = {
                    "message": 'success',
                    "account": account.__dict__
            }
            transaction.state = 'Success'
            self.transaction_db.create_transaction(transaction)
            return response, 200
        else:
            response = {
                    "message": 'Account not found'
            }
            return response, 404



@api.route('/<id>')
class TransactionIdController(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transaction_db = TransactionDb(current_app.config.get('DB_PARAMS'))

    @api.response(200, "Request success")
    def get(self, id):
        return self.transaction_db.get_transaction(id), 200