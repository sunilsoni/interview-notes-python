from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Tuple


class Transaction:
    def __init__(self, account_id: str, amount: float, timestamp: datetime, location: str):
        self.account_id = account_id
        self.amount = amount
        self.timestamp = timestamp
        self.location = location

    def __repr__(self):
        return f"Transaction(account={self.account_id}, amount=${self.amount}, time={self.timestamp}, location={self.location})"


class TransactionProcessor:
    def __init__(self,
                 amount_threshold: float = 5000.0,
                 count_threshold: int = 5,
                 time_window_minutes: int = 10):
        # Configuration
        self.amount_threshold = amount_threshold
        self.count_threshold = count_threshold
        self.time_window = timedelta(minutes=time_window_minutes)

        # Storage for transaction history per account
        self.transaction_history: Dict[str, List[Transaction]] = defaultdict(list)

    def process_transaction(self, transaction: Transaction) -> Tuple[bool, str]:
        """
        Process a transaction and determine if it should be allowed or blocked.

        Args:
            transaction: Transaction object to process

        Returns:
            Tuple of (is_allowed: bool, message: str)
        """
        account_id = transaction.account_id

        # Add transaction to history
        self.transaction_history[account_id].append(transaction)

        # Clean up old transactions outside the time window
        self._cleanup_old_transactions(account_id, transaction.timestamp)

        # Get recent transactions within the time window
        recent_transactions = self._get_recent_transactions(account_id, transaction.timestamp)

        # Check all fraud detection rules
        rule_violations = []

        # Rule 1: Check amount aggregation
        if self._check_amount_rule(recent_transactions):
            rule_violations.append("Amount threshold exceeded ($5000 in 10 minutes)")

        # Rule 2: Check transaction count
        if self._check_count_rule(recent_transactions):
            rule_violations.append("Too many transactions (>5 in 10 minutes)")

        # Rule 3: Check geographic anomaly
        if self._check_location_rule(recent_transactions):
            rule_violations.append("Multiple locations detected in 10 minutes")

        # Make decision
        if rule_violations:
            message = f"TRANSACTION BLOCKED for account {account_id}\n"
            message += f"Transaction: {transaction}\n"
            message += f"Reasons: {', '.join(rule_violations)}"
            return False, message
        else:
            message = f"TRANSACTION ALLOWED for account {account_id}\n"
            message += f"Transaction: {transaction}"
            return True, message

    def _cleanup_old_transactions(self, account_id: str, current_time: datetime):
        """Remove transactions older than the time window."""
        cutoff_time = current_time - self.time_window
        self.transaction_history[account_id] = [
            t for t in self.transaction_history[account_id]
            if t.timestamp >= cutoff_time
        ]

    def _get_recent_transactions(self, account_id: str, current_time: datetime) -> List[Transaction]:
        """Get transactions within the time window."""
        cutoff_time = current_time - self.time_window
        return [
            t for t in self.transaction_history[account_id]
            if t.timestamp >= cutoff_time
        ]

    def _check_amount_rule(self, transactions: List[Transaction]) -> bool:
        """Rule 1: Check if total amount exceeds threshold."""
        total_amount = sum(t.amount for t in transactions)
        return total_amount > self.amount_threshold

    def _check_count_rule(self, transactions: List[Transaction]) -> bool:
        """Rule 2: Check if transaction count exceeds threshold."""
        return len(transactions) > self.count_threshold

    def _check_location_rule(self, transactions: List[Transaction]) -> bool:
        """Rule 3: Check if transactions occur from multiple locations."""
        unique_locations = set(t.location for t in transactions)
        return len(unique_locations) > 1


# Example usage and testing
if __name__ == "__main__":
    # Create processor instance
    processor = TransactionProcessor()

    # Test Case 1: Normal transactions (should be allowed)
    print("=" * 60)
    print("TEST CASE 1: Normal Transactions")
    print("=" * 60)

    t1 = Transaction("ACC123", 100.0, datetime.now(), "New York")
    allowed, msg = processor.process_transaction(t1)
    print(msg)
    print()

    # Test Case 2: Amount threshold violation
    print("=" * 60)
    print("TEST CASE 2: Amount Threshold Violation")
    print("=" * 60)

    processor2 = TransactionProcessor()
    base_time = datetime.now()

    t2 = Transaction("ACC456", 2000.0, base_time, "Los Angeles")
    allowed, msg = processor2.process_transaction(t2)
    print(msg)
    print()

    t3 = Transaction("ACC456", 2500.0, base_time + timedelta(minutes=3), "Los Angeles")
    allowed, msg = processor2.process_transaction(t3)
    print(msg)
    print()

    t4 = Transaction("ACC456", 1000.0, base_time + timedelta(minutes=5), "Los Angeles")
    allowed, msg = processor2.process_transaction(t4)
    print(msg)
    print()

    # Test Case 3: Transaction count violation
    print("=" * 60)
    print("TEST CASE 3: Transaction Count Violation")
    print("=" * 60)

    processor3 = TransactionProcessor()
    base_time = datetime.now()

    for i in range(6):
        t = Transaction("ACC789", 50.0, base_time + timedelta(minutes=i), "Chicago")
        allowed, msg = processor3.process_transaction(t)
        print(f"Transaction {i + 1}:")
        print(msg)
        print()

    # Test Case 4: Location anomaly
    print("=" * 60)
    print("TEST CASE 4: Geographic Anomaly")
    print("=" * 60)

    processor4 = TransactionProcessor()
    base_time = datetime.now()

    t5 = Transaction("ACC999", 100.0, base_time, "Miami")
    allowed, msg = processor4.process_transaction(t5)
    print(msg)
    print()

    t6 = Transaction("ACC999", 150.0, base_time + timedelta(minutes=5), "Seattle")
    allowed, msg = processor4.process_transaction(t6)
    print(msg)
    print()

    # Test Case 5: Multiple rule violations
    print("=" * 60)
    print("TEST CASE 5: Multiple Rule Violations")
    print("=" * 60)

    processor5 = TransactionProcessor()
    base_time = datetime.now()

    for i in range(7):
        location = "Boston" if i % 2 == 0 else "Denver"
        t = Transaction("ACC111", 900.0, base_time + timedelta(minutes=i), location)
        allowed, msg = processor5.process_transaction(t)
        print(f"Transaction {i + 1}:")
        print(msg)
        print()
