from typing import Optional, Dict, List
from banking_system import BankingSystem


class Account:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        self.outgoing = 0  # <--- CRITICAL CHANGE 1: Track outgoing funds


class BankingSystemImpl(BankingSystem):
    def __init__(self):
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

        # <--- CRITICAL CHANGE 2: Increment outgoing tracker
        source_acc.outgoing += amount

        return source_acc.balance

    def top_spenders(self, timestamp: int, n: int) -> List[str]:
        # <--- CRITICAL CHANGE 3: Implement sorting logic

        # 1. Get all accounts
        all_accounts = list(self.accounts.values())

        # 2. Sort by Outgoing (Desc) and Account ID (Asc)
        # We use -acc.outgoing for descending sort
        sorted_accounts = sorted(all_accounts, key=lambda acc: (-acc.outgoing, acc.account_id))

        # 3. Take top n
        top_n = sorted_accounts[:n]

        # 4. Format as strings ["id(amount)", ...]
        return [f"{acc.account_id}({acc.outgoing})" for acc in top_n]