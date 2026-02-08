import sys
import time
from typing import Optional


class BankingSystemImpl:
    def __init__(self):
        # Dictionary for O(1) access
        # Key: account_id (str), Value: balance (int)
        self.accounts = {}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Creates a new account with the given identifier if it doesn't already exist.
        Returns True if successful, False if account already exists.
        """
        if account_id in self.accounts:
            return False
        self.accounts[account_id] = 0
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        """
        Deposits the given amount into the specified account.
        Returns the new balance or None if account doesn't exist.
        """
        if account_id not in self.accounts:
            return None

        self.accounts[account_id] += amount
        return self.accounts[account_id]

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> Optional[int]:
        """
        Transfers money between two different accounts.
        Returns the source account balance after transfer or None if failed.
        """
        # Check 1: Source or Target account doesn't exist
        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None

        # Check 2: Cannot transfer to self
        if source_account_id == target_account_id:
            return None

        # Check 3: Insufficient funds
        if self.accounts[source_account_id] < amount:
            return None

        # Execute Transfer
        self.accounts[source_account_id] -= amount
        self.accounts[target_account_id] += amount

        return self.accounts[source_account_id]


def run_tests():
    """
    Main method to verify correctness and performance.
    """
    bs = BankingSystemImpl()

    print("--- Running Standard Test Cases ---")

    # Helper to assert results
    def expect(case_name, result, expected_val):
        status = "PASS" if result == expected_val else f"FAIL (Got {result}, Expected {expected_val})"
        print(f"{case_name}: {status}")

    # Case 1: Account Creation
    expect("Create acc1", bs.create_account(1, "acc1"), True)
    expect("Create acc2", bs.create_account(2, "acc2"), True)
    expect("Create duplicate acc1", bs.create_account(3, "acc1"), False)

    # Case 2: Deposits
    expect("Deposit to non-existent", bs.deposit(4, "acc_x", 100), None)
    expect("Deposit to acc1", bs.deposit(5, "acc1", 1000), 1000)
    expect("Deposit to acc2", bs.deposit(6, "acc2", 2000), 2000)

    # Case 3: Transfers
    expect("Transfer invalid source", bs.transfer(7, "acc_x", "acc2", 100), None)
    expect("Transfer invalid target", bs.transfer(8, "acc1", "acc_y", 100), None)
    expect("Transfer same account", bs.transfer(9, "acc1", "acc1", 100), None)
    expect("Transfer insufficient funds", bs.transfer(10, "acc1", "acc2", 5000), None)
    expect("Transfer success", bs.transfer(11, "acc1", "acc2", 500), 500)  # 1000 - 500 = 500 Remaining in acc1

    # Verify balances after transfer
    # acc1 should be 500, acc2 should be 2000 + 500 = 2500
    expect("Check acc1 balance", bs.deposit(12, "acc1", 0), 500)
    expect("Check acc2 balance", bs.deposit(13, "acc2", 0), 2500)

    print("\n--- Running Large Data Input Test ---")

    bs_perf = BankingSystemImpl()
    num_accounts = 100000

    start_time = time.time()

    # 1. Bulk Creation
    for i in range(num_accounts):
        bs_perf.create_account(i, f"user_{i}")

    # 2. Setup user_0 with funds
    bs_perf.deposit(num_accounts, "user_0", num_accounts)

    # 3. Bulk Transfer (user_0 sends 1 unit to every other user)
    # Range is 1 to num_accounts-1
    for i in range(1, num_accounts):
        bs_perf.transfer(num_accounts + i, "user_0", f"user_{i}", 1)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Processed {num_accounts} creations and {num_accounts} transfers in {duration:.4f} seconds.")

    # Check final state
    final_bal_user0 = bs_perf.deposit(999999, "user_0", 0)
    # user_0 started with 100,000. Transferred 1 to (100,000 - 1) users.
    # Remaining should be 1.
    expect("Large Scale Logic Check", final_bal_user0, 1)

    if duration < 3.0:
        print("PERFORMANCE: PASS (Under 3 seconds)")
    else:
        print("PERFORMANCE: FAIL (Too slow)")


if __name__ == "__main__":
    run_tests()