from banking_system import BankingSystem


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self._balances = {}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self._balances:
            return False
        self._balances[account_id] = 0
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        bal = self._balances.get(account_id)
        if bal is None:
            return None
        bal += amount
        self._balances[account_id] = bal
        return bal

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        bal = self._balances.get(account_id)
        if bal is None or amount > bal:
            return None
        bal -= amount
        self._balances[account_id] = bal
        return bal