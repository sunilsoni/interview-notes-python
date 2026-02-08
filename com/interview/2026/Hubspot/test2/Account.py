# ==========================================
# 2. Implementation (Updated for Level 2)
# ==========================================

class Account:
    """
    Updated Account class to track outgoing transaction totals.
    """
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        self.outgoing = 0  # New for Level 2: Tracks total outgoing transfers