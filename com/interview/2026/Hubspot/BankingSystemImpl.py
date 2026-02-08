class BankingSystemImpl(BankingSystem):
    def __init__(self):
        # Using a dictionary for O(1) access time
        # Key: account_id (str), Value: Account object
        self.accounts: Dict[str, Account] = {}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Creates a new account. Returns False if it already exists.
        """
        if account_id in self.accounts:
            return False

        self.accounts[account_id] = Account(account_id)
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        """
        Deposits money. Returns new balance or None if account missing.
        """
        if account_id not in self.accounts:
            return None

        account = self.accounts[account_id]
        account.balance += amount
        return account.balance

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> Optional[int]:
        """
        Transfers money. Returns source balance after transfer or None if failed.
        """
        # Check 1: Accounts must exist
        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None

        # Check 2: Cannot transfer to self
        if source_account_id == target_account_id:
            return None

        source_acc = self.accounts[source_account_id]
        target_acc = self.accounts[target_account_id]

        # Check 3: Insufficient funds
        if source_acc.balance < amount:
            return None

        # Execute Transfer
        source_acc.balance -= amount
        target_acc.balance += amount

        return source_acc.balance