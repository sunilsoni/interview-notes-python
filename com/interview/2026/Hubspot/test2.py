import sys
import time
from typing import Optional, Dict


class Account:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        # Level 2 Preparation: We can easily add self.outgoing = 0 here later
        # Level 4 Preparation: We can easily add self.history = [] here later


class BankingSystemImpl:
    def __init__(self):
        # Key: account_id (str), Value: Account object
        # This structure allows adding complexity to 'Account' without breaking the map
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

        source = self.accounts[source_account_id]
        target = self.accounts[target_account_id]

        if source.balance < amount:
            return None

        # Execute Transfer
        source.balance -= amount
        target.balance += amount

        # Level 2 Note: Here we will just add 'source.outgoing += amount' later

        return source.balance


def run_tests():
    bs = BankingSystemImpl()
    print("--- Running Standard Test Cases (Extensible Version) ---")

    def expect(case_name, result, expected_val):
        status = "PASS" if result == expected_val else f"FAIL (Got {result}, Expected {expected_val})"
        print(f"{case_name}: {status}")

    # Standard Logic Checks
    expect("Create acc1", bs.create_account(1, "acc1"), True)
    expect("Create acc2", bs.create_account(2, "acc2"), True)
    expect("Deposit acc1", bs.deposit(3, "acc1", 1000), 1000)
    expect("Deposit acc2", bs.deposit(4, "acc2", 1000), 1000)
    expect("Transfer success", bs.transfer(5, "acc1", "acc2", 500), 500)
    expect("Transfer fail (funds)", bs.transfer(6, "acc1", "acc2", 600), None)

    # Large Data Performance Check
    print("\n--- Running Large Data Input Test ---")
    bs_perf = BankingSystemImpl()
    num_accounts = 100000
    start = time.time()

    for i in range(num_accounts):
        bs_perf.create_account(i, f"u_{i}")
    bs_perf.deposit(num_accounts, "u_0", num_accounts)
    for i in range(1, num_accounts):
        bs_perf.transfer(num_accounts + i, "u_0", f"u_{i}", 1)

    duration = time.time() - start
    print(f"Processed 200k+ ops in {duration:.4f}s")

    if duration < 3.0:
        print("PERFORMANCE: PASS")
    else:
        print("PERFORMANCE: FAIL")


if __name__ == "__main__":
    run_tests()