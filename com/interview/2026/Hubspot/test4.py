from typing import Optional, Dict, List
from banking_system import BankingSystem


class Account:
    """
    Helper class to store account details.
    """

    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        self.outgoing = 0  # ### LEVEL 2 CHANGE: Track total outgoing transfers ###


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        # Key: account_id (str), Value: Account object
        self.accounts: Dict[str, Account] = {}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = Account(account_id)
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        if account_id not in self.accounts:
            return None

        account = self.accounts[account_id]
        account.balance += amount
        return account.balance

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> Optional[int]:
        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None

        if source_account_id == target_account_id:
            return None

        source_acc = self.accounts[source_account_id]
        target_acc = self.accounts[target_account_id]

        if source_acc.balance < amount:
            return None

        # Execute Transfer
        source_acc.balance -= amount
        target_acc.balance += amount

        # ### LEVEL 2 CHANGE: Increment outgoing tracker on successful transfer ###
        source_acc.outgoing += amount

        return source_acc.balance

    # ### LEVEL 2 CHANGE: Implement the top_spenders method ###
    def top_spenders(self, timestamp: int, n: int) -> List[str]:
        """
        Returns top 'n' accounts by outgoing transactions.
        Sorted by outgoing amount (descending), then account_id (ascending).
        """
        # 1. Get all accounts
        all_accounts = list(self.accounts.values())

        # 2. Sort
        # We use (-acc.outgoing) for descending sort on amount
        # We use (acc.account_id) for ascending sort on ID (alphabetical)
        sorted_accounts = sorted(all_accounts, key=lambda acc: (-acc.outgoing, acc.account_id))

        # 3. Slice top n
        top_n = sorted_accounts[:n]

        # 4. Format output string
        result = [f"{acc.account_id}({acc.outgoing})" for acc in top_n]

        return result