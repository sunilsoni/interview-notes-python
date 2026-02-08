from typing import Optional, Dict, List, Tuple
import heapq
from banking_system import BankingSystem


class Account:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        self.outgoing = 0


class Payment:
    def __init__(self, payment_id: str, account_id: str, cashback_amount: int, due_time: int):
        self.payment_id = payment_id
        self.account_id = account_id
        self.cashback_amount = cashback_amount
        self.due_time = due_time
        self.status = "IN_PROGRESS"


class BankingSystemImpl(BankingSystem):

    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.payment_counter = 0
        self.payments: Dict[str, Payment] = {}
        self.scheduled_cashbacks: List[Tuple[int, str]] = []  # Fixed spelling to 'cashbacks'

    def _process_pending_cashbacks(self, current_timestamp: int):
        # Loop while there are items and the earliest one is due
        while self.scheduled_cashbacks and self.scheduled_cashbacks[0][0] <= current_timestamp:
            due_time, payment_id = heapq.heappop(self.scheduled_cashbacks)

            # Retrieve payment
            if payment_id in self.payments:
                payment = self.payments[payment_id]

                # Double check status to avoid double paying (safety)
                if payment.status == "IN_PROGRESS":
                    if payment.account_id in self.accounts:
                        self.accounts[payment.account_id].balance += payment.cashback_amount

                    payment.status = "CASHBACK_RECEIVED"

    def create_account(self, timestamp: int, account_id: str) -> bool:
        self._process_pending_cashbacks(timestamp)  # <--- ADDED THIS LINE (Crucial)

        if account_id in self.accounts:
            return False
        self.accounts[account_id] = Account(account_id)
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        self._process_pending_cashbacks(timestamp)  # <--- ADDED THIS LINE (Crucial for test failures)

        if account_id not in self.accounts:
            return None
        account = self.accounts[account_id]
        account.balance += amount
        return account.balance

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        self._process_pending_cashbacks(timestamp)  # <--- ADDED THIS LINE (Crucial)

        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None
        if source_account_id == target_account_id:
            return None

        source_acc = self.accounts[source_account_id]
        target_acc = self.accounts[target_account_id]

        if source_acc.balance < amount:
            return None

        source_acc.balance -= amount
        target_acc.balance += amount
        source_acc.outgoing += amount

        return source_acc.balance

    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        self._process_pending_cashbacks(timestamp)  # <--- ADDED THIS LINE

        all_accounts = list(self.accounts.values())
        # Sort by outgoing (descending) and account_id (ascending)
        sorted_accounts = sorted(all_accounts, key=lambda acc: (-acc.outgoing, acc.account_id))
        top_n_accounts = sorted_accounts[:n]

        result = [f"{acc.account_id}({acc.outgoing})" for acc in top_n_accounts]
        return result

    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        self._process_pending_cashbacks(timestamp)  # <--- You already had this, keep it.

        if account_id not in self.accounts:
            return None

        account = self.accounts[account_id]

        if account.balance < amount:
            return None

        account.balance -= amount
        account.outgoing += amount

        self.payment_counter += 1
        payment_id = f"payment{self.payment_counter}"

        cashback_amt = int(amount * 0.02)
        wait_period = 86400000
        due_time = timestamp + wait_period

        new_payment = Payment(payment_id, account_id, cashback_amt, due_time)
        self.payments[payment_id] = new_payment

        heapq.heappush(self.scheduled_cashbacks, (due_time, payment_id))

        return payment_id

    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        self._process_pending_cashbacks(timestamp)  # <--- ADDED THIS LINE (Crucial for status checks)

        if account_id not in self.accounts:
            return None
        if payment not in self.payments:
            return None

        payment_obj = self.payments[payment]

        if payment_obj.account_id != account_id:
            return None

        return payment_obj.status