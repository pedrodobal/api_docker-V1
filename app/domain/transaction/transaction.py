import uuid
import time

class Transaction:

    def __init__(self, merchant, amount, state, accountID):
        self.transaction_id = str(uuid.uuid4())
        self.account_id = accountID
        self.merchant = merchant
        self.amount = amount
        self.state = state
        self.transaction_time = int(time.time())