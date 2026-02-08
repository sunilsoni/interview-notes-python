import sys
from abc import ABC, abstractmethod
from typing import Optional, Dict, List


# ==========================================
# 1. THE INTERFACE (BankingSystem)
# ==========================================
class BankingSystem(ABC):
    @abstractmethod
    def create_account(self, timestamp: int, account_id: str) -> bool:
        pass

    @abstractmethod
    def deposit(self, timestamp: int, account_id: str, amount: int) -> Optional[int]:
        pass

    @abstractmethod
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> Optional[int]:
        pass

    @abstractmethod
    def top_spenders(self, timestamp: int, n: int) -> List[str]:
        pass


# ==========================================
# 2. THE FIXED IMPLEMENTATION (BankingSystemImpl)
# ==========================================
class Account:
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.balance = 0
        self.outgoing = 0  # <--- CRITICAL FIX: Tracks outgoing funds


class BankingSystemImpl(BankingSystem):
    def __init__(self):
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

        # <--- CRITICAL FIX: Increment outgoing tracker
        source_acc.outgoing += amount

        return source_acc.balance

    def top_spenders(self, timestamp: int, n: int) -> List[str]:
        """
        Returns top 'n' accounts by outgoing transactions.
        Sort: Descending by outgoing amount, then Ascending by account_id.
        """
        # 1. Get all accounts
        all_accounts = list(self.accounts.values())

        # 2. Sort by Outgoing (Desc) and Account ID (Asc)
        # We use -acc.outgoing to sort descending (highest first)
        # We use acc.account_id to break ties alphabetically (A before B)
        sorted_accounts = sorted(all_accounts, key=lambda acc: (-acc.outgoing, acc.account_id))

        # 3. Take top n
        top_n = sorted_accounts[:n]

        # 4. Format as strings ["id(amount)", ...]
        return [f"{acc.account_id}({acc.outgoing})" for acc in top_n]


# ==========================================
# 3. VERIFICATION (Recreating your Failed Tests)
# ==========================================
def run_verification():
    print("--- Verifying Fix with Actual Test Cases ---\n")

    # Helper to check results
    def assert_equal(test_name, actual, expected):
        if actual == expected:
            print(f"✅ {test_name}: PASS")
        else:
            print(f"❌ {test_name}: FAIL")
            print(f"   Expected: {expected}")
            print(f"   Got:      {actual}")

    # ---------------------------------------------------------
    # TEST CASE 1: Based on 'test_level_2_case_01' logic
    # ---------------------------------------------------------
    bs = BankingSystemImpl()
    bs.create_account(1, "account1")
    bs.create_account(2, "account2")
    bs.create_account(3, "account3")

    bs.deposit(4, "account1", 1000)
    bs.deposit(5, "account2", 1000)
    bs.deposit(6, "account3", 1000)

    # Perform transfers to generate 'outgoing' data
    # Scenario:
    # account2 sends 100 to account3 -> acc2 outgoing = 100
    # account3 sends 50 to account1  -> acc3 outgoing = 50
    # account2 sends 100 to account1 -> acc2 outgoing = 200

    bs.transfer(7, "account2", "account3", 100)
    bs.transfer(8, "account3", "account1", 50)
    bs.transfer(9, "account2", "account1", 100)

    # Expected Ranking:
    # 1. account2 (200 outgoing)
    # 2. account3 (50 outgoing)
    # 3. account1 (0 outgoing)

    expected_1 = ['account2(200)', 'account3(50)', 'account1(0)']
    assert_equal("Case 01 (Basic Logic)", bs.top_spenders(10, 3), expected_1)

    # ---------------------------------------------------------
    # TEST CASE 2: Alphabetical Tie-Breaking
    # ---------------------------------------------------------
    bs2 = BankingSystemImpl()
    bs2.create_account(1, "accB")
    bs2.create_account(2, "accA")
    bs2.create_account(3, "accC")

    bs2.deposit(4, "accA", 1000)
    bs2.deposit(5, "accB", 1000)
    bs2.deposit(6, "accC", 1000)

    # Everyone spends exactly 100
    bs2.transfer(7, "accA", "accB", 100)
    bs2.transfer(8, "accB", "accC", 100)
    bs2.transfer(9, "accC", "accA", 100)

    # Since amounts are equal (100), should sort alphabetically: accA, accB, accC
    expected_2 = ['accA(100)', 'accB(100)', 'accC(100)']
    assert_equal("Case 02 (Tie-Breaking)", bs2.top_spenders(10, 3), expected_2)

    # ---------------------------------------------------------
    # TEST CASE 3: Large Data / Empty Return Bug Check
    # ---------------------------------------------------------
    bs3 = BankingSystemImpl()
    bs3.create_account(1, "u1")
    bs3.deposit(2, "u1", 100)
    # No transfers made. Should return u1(0).
    # If your bug persists, this would return []
    expected_3 = ['u1(0)']
    assert_equal("Case 03 (Zero Spenders)", bs3.top_spenders(3, 1), expected_3)


if __name__ == "__main__":
    run_verification()