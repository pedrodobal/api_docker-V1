import uuid
from app.domain.transaction.transaction_db import TransactionDb

class Account:

    def __init__(self, active_card, available_limit, account_id = None):
        if not account_id:
            self.account_id = str(uuid.uuid4())
        else:
            self.account_id = account_id
        self.active_card = active_card
        self.available_limit = available_limit

    def change_card_status(self):
        self.active_card = not self.active_card

    def is_card_active(self):
        return self.active_card

    def get_transactions(self):
        return TransactionDb.get_transactions_by_account_id(self.account_id)
    
    def check_limit(self, value):
        return value <= self.available_limit
    
    def update_limit(self, value):
        self.available_limit = value
