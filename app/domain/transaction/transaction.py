import uuid
import time

class Transaction:

    def __init__(self, merchant, amount, state, accountID):
        self.transactionId = str(uuid.uuid4())
        self.accountId = accountID
        self.merchant = merchant
        self.amount = amount
        self.state = state
        self.transactionTime = int(time.time())