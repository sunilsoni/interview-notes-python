# ==========================================
# 2. Implementation (banking_system_impl.py)
# ==========================================

class Account:
    """
    Helper class to store account details.
    This makes the system extensible for future levels (Ranking, Merging, etc.).
    """
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        # Future extensibility:
        # self.outgoing_transactions = 0  (Level 2)
        # self.scheduled_payments = []    (Level 3)