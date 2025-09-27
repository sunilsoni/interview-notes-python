from banking_system import BankingSystem


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        # account_id -> current balance
        self._balances: dict[str, int] = {}
        # account_id -> cumulative transaction value (deposits + successful withdrawals)
        self._activity: dict[str, int] = {}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self._balances:
            return False
        self._balances[account_id] = 0
        self._activity[account_id] = 0
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self._balances or amount < 0:
            return None
        new_bal = self._balances[account_id] + amount
        self._balances[account_id] = new_bal
        self._activity[account_id] += amount
        return new_bal

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if amount < 0:
            return None
        bal = self._balances.get(account_id)
        if bal is None or bal < amount:
            return None
        new_bal = bal - amount
        self._balances[account_id] = new_bal
        self._activity[account_id] += amount
        return new_bal

    def top_activity(self, timestamp: int, n: int) -> list[str]:
        # Sort by total transaction value desc, then account_id asc
        items = [(acc, self._activity.get(acc, 0)) for acc in self._balances]
        items.sort(key=lambda x: (-x[1], x[0]))
        take = min(n, len(items))
        return [f"{acc}({val})" for acc, val in items[:take]]