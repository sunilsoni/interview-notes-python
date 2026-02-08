from typing import Optional, Dict, List


class Account:
    """
    Helper class to store account details.
    """

    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        self.outgoing = 0  # Tracks total outgoing transfers for Level 2


class BankingSystemImpl:
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

        # Level 2 Requirement: Track outgoing transactions
        source_acc.outgoing += amount

        return source_acc.balance

    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        """
        Should return the identifiers of the top `n` accounts with
        the highest outgoing transactions - the total amount of
        money either transferred out of or paid/withdrawn (the
        **pay** operation will be introduced in level 3) - sorted in
        descending order, or in case of a tie, sorted alphabetically
        by `account_id` in ascending order.
        The result should be a list of strings in the following
        format: `["<account_id_1>(<total_outgoing_1>)", "<account_id
        _2>(<total_outgoing_2>)", ..., "<account_id_n>(<total_outgoi
        ng_n>)"]`.
          * If less than `n` accounts exist in the system, then return
          all their identifiers (in the described format).
          * Cashback (an operation that will be introduced in level 3)
          should not be reflected in the calculations for total
          outgoing transactions.
        """
        # 1. Get all accounts list
        all_accounts = list(self.accounts.values())

        # 2. Sort accounts based on requirements:
        #    Primary Key: Outgoing amount (Descending) -> -acc.outgoing
        #    Secondary Key: Account ID (Ascending/Alphabetical) -> acc.account_id
        sorted_accounts = sorted(all_accounts, key=lambda acc: (-acc.outgoing, acc.account_id))

        # 3. Take the top n accounts
        top_n_accounts = sorted_accounts[:n]

        # 4. Format the output strings
        result = [f"{acc.account_id}({acc.outgoing})" for acc in top_n_accounts]

        return result