import uuid
from app.domain.transaction.transaction_db import TransactionDb

class Account:

    def __init__(self, active_card, available_limit, account_id = None):
        if not account_id:
            self.accountId = str(uuid.uuid4())
        else:
            self.accountId = account_id
        self.activeCard = active_card
        self.availableLimit = available_limit

    def changeCardStatus(self):
        self.activeCard = not self.activeCard

    def isCardActive(self):
        return self.activeCard

    def getTransactions(self):
        return TransactionDb.get_transactions_by_account_id(self.accountId)
    
    def checkLimit(self, value):
        return value <= self.availableLimit
    
    def updateLimit(self, value):
        self.availableLimit = value
