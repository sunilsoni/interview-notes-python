import heapq
from typing import Optional, Dict, List, Tuple
from banking_system import BankingSystem


class Account:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        self.outgoing = 0  # Tracks total outgoing (transfers + payments)


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

        # Level 3: Payment tracking
        self.payment_counter = 0
        self.payments: Dict[str, Payment] = {}

        # Priority Queue for scheduled cashbacks: stores tuples (due_time, payment_id)
        # Using a heap allows efficient retrieval of the "next due" cashback
        self.scheduled_cashbacks: List[Tuple[int, str]] = []

    def _process_pending_cashbacks(self, current_timestamp: int):
        """
        Internal helper: Process all cashbacks scheduled for <= current_timestamp.
        Must be called at the start of EVERY public method.
        """
        while self.scheduled_cashbacks and self.scheduled_cashbacks[0][0] <= current_timestamp:
            # Pop the earliest scheduled cashback
            due_time, payment_id = heapq.heappop(self.scheduled_cashbacks)

            payment = self.payments[payment_id]

            # Apply cashback if account still exists (Edge case, though delete isn't in spec)
            if payment.account_id in self.accounts:
                self.accounts[payment.account_id].balance += payment.cashback_amount

            # Update status
            payment.status = "CASHBACK_RECEIVED"

    def create_account(self, timestamp: int, account_id: str) -> bool:
        self._process_pending_cashbacks(timestamp)  # Level 3 Check

        if account_id in self.accounts:
            return False
        self.accounts[account_id] = Account(account_id)
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        self._process_pending_cashbacks(timestamp)  # Level 3 Check

        if account_id not in self.accounts:
            return None

        account = self.accounts[account_id]
        account.balance += amount
        return account.balance

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> Optional[int]:
        self._process_pending_cashbacks(timestamp)  # Level 3 Check

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
        source_acc.outgoing += amount

        return source_acc.balance

    def top_spenders(self, timestamp: int, n: int) -> List[str]:
        self._process_pending_cashbacks(timestamp)  # Level 3 Check

        all_accounts = list(self.accounts.values())
        # Sort: Outgoing (Desc), Account ID (Asc)
        sorted_accounts = sorted(all_accounts, key=lambda acc: (-acc.outgoing, acc.account_id))
        top_n = sorted_accounts[:n]
        return [f"{acc.account_id}({acc.outgoing})" for acc in top_n]

    # --- LEVEL 3 NEW METHODS ---

    def pay(self, timestamp: int, account_id: str, amount: int) -> Optional[str]:
        self._process_pending_cashbacks(timestamp)  # Ensure any due cashbacks happen first

        if account_id not in self.accounts:
            return None

        account = self.accounts[account_id]

        if account.balance < amount:
            return None

        # 1. Process Withdrawal
        account.balance -= amount
        account.outgoing += amount  # Payments count towards "outgoing"

        # 2. Generate Payment ID
        self.payment_counter += 1
        payment_id = f"payment{self.payment_counter}"

        # 3. Calculate Cashback (2% rounded down)
        cashback_amt = int(amount * 0.02)

        # 4. Schedule Cashback (Current Time + 24 hours in ms)
        wait_period = 86400000  # 24 * 60 * 60 * 1000
        due_time = timestamp + wait_period

        # 5. Store Payment Info
        new_payment = Payment(payment_id, account_id, cashback_amt, due_time)
        self.payments[payment_id] = new_payment

        # 6. Add to Priority Queue
        heapq.heappush(self.scheduled_cashbacks, (due_time, payment_id))

        return payment_id

    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> Optional[str]:
        self._process_pending_cashbacks(timestamp)  # Ensure status is up-to-date

        if account_id not in self.accounts:
            return None

        if payment not in self.payments:
            return None

        payment_obj = self.payments[payment]

        if payment_obj.account_id != account_id:
            return None

        return payment_obj.status