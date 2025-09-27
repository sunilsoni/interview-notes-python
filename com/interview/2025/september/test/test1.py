from banking_system import BankingSystem

# 🟢 GREEN BUTTON: expiry window (24h in ms). Change only if spec changes.
MS_IN_DAY = 24 * 60 * 60 * 1000  # 86,400,000 ms


class BankingSystemImpl(BankingSystem):
    def __init__(self):
        self._balances: dict[str, int] = {}
        self._activity: dict[str, int] = {}

        # 🟢 GREEN BUTTON: transfer storage (id -> record)
        self._transfers: dict[str, dict] = {}
        self._next_tid: int = 1

    # ---------- internals ----------
    def _expire_transfers_until(self, now_ts: int) -> None:
        """
        Refund only transfers that are still pending and whose 24h window
        has fully elapsed. Transfer expires at the *next* millisecond after 24h.
        """
        # 🟢 GREEN BUTTON: expiry boundary rule (+ MS_IN_DAY + 1)
        for t in self._transfers.values():
            if t["status"] == "pending" and now_ts >= t["created"] + MS_IN_DAY + 1:
                self._balances[t["src"]] += t["amount"]
                t["status"] = "expired"

    # ---------- level 1 ----------
    def create_account(self, timestamp: int, account_id: str) -> bool:
        self._expire_transfers_until(timestamp)
        if account_id in self._balances:
            return False
        self._balances[account_id] = 0
        self._activity[account_id] = 0
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._expire_transfers_until(timestamp)
        if amount < 0 or account_id not in self._balances:
            return None
        new_bal = self._balances[account_id] + amount
        self._balances[account_id] = new_bal
        self._activity[account_id] += amount
        return new_bal

    def pay(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._expire_transfers_until(timestamp)
        if amount < 0:
            return None
        bal = self._balances.get(account_id)
        if bal is None or bal < amount:
            return None
        new_bal = bal - amount
        self._balances[account_id] = new_bal
        self._activity[account_id] += amount
        return new_bal

    # ---------- level 2 ----------
    def top_activity(self, timestamp: int, n: int) -> list[str]:
        self._expire_transfers_until(timestamp)
        items = [(acc, self._activity.get(acc, 0)) for acc in self._balances.keys()]
        # 🟢 GREEN BUTTON: sort rule (value desc, id asc)
        items.sort(key=lambda x: (-x[1], x[0]))
        k = min(n, len(items))
        # 🟢 GREEN BUTTON: exact output format (no space before '(')
        return [f"{acc}({val})" for acc, val in items[:k]]

    # ---------- level 3 ----------
    def transfer(
        self,
        timestamp: int,
        source_account_id: str,
        target_account_id: str,
        amount: int,
    ) -> str | None:
        self._expire_transfers_until(timestamp)

        # 🟢 GREEN BUTTON: validation rules
        if (
            amount < 0
            or source_account_id == target_account_id
            or source_account_id not in self._balances
            or target_account_id not in self._balances
        ):
            return None
        if self._balances[source_account_id] < amount:
            return None

        # Withhold from source and create a pending transfer
        self._balances[source_account_id] -= amount
        # 🟢 GREEN BUTTON: transfer id format
        tid = f"transfer{self._next_tid}"
        self._next_tid += 1

        self._transfers[tid] = {
            "src": source_account_id,
            "tgt": target_account_id,
            "amount": amount,
            "created": timestamp,
            "status": "pending",
        }
        return tid

    def accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool:
        self._expire_transfers_until(timestamp)

        t = self._transfers.get(transfer_id)
        if not t or t["status"] != "pending":
            return False
        if t["tgt"] != account_id:
            return False

        # If it expired exactly now, helper already refunded & marked expired
        if timestamp >= t["created"] + MS_IN_DAY + 1:
            return False

        # 🟢 GREEN BUTTON: single credit to target on acceptance
        self._balances[t["tgt"]] += t["amount"]
        # 🟢 GREEN BUTTON: transfers count toward activity only when accepted
        self._activity[t["src"]] += t["amount"]
        self._activity[t["tgt"]] += t["amount"]
        t["status"] = "accepted"
        return True