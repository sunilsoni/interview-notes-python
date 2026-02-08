# ==========================================
# 3. Test Runner (main method)
# ==========================================
def run_tests():
    bs = BankingSystemImpl()
    print("--- Running Level 1 Tests ---")

    def expect(case_name, result, expected_val):
        # Helper to print PASS/FAIL status
        status = "PASS" if result == expected_val else f"FAIL (Got {result}, Expected {expected_val})"
        print(f"{case_name}: {status}")

    # --- Basic Functional Tests ---
    expect("Create acc1", bs.create_account(1, "acc1"), True)
    expect("Create acc2", bs.create_account(2, "acc2"), True)
    expect("Create duplicate acc1", bs.create_account(3, "acc1"), False)

    expect("Deposit to non-existent", bs.deposit(4, "acc_x", 100), None)
    expect("Deposit to acc1", bs.deposit(5, "acc1", 1000), 1000)
    expect("Deposit to acc2", bs.deposit(6, "acc2", 2000), 2000)

    expect("Transfer invalid source", bs.transfer(7, "acc_x", "acc2", 100), None)
    expect("Transfer same account", bs.transfer(9, "acc1", "acc1", 100), None)
    expect("Transfer insufficient funds", bs.transfer(10, "acc1", "acc2", 5000), None)
    expect("Transfer success", bs.transfer(11, "acc1", "acc2", 500), 500)  # 1000 - 500 = 500 left

    # --- Large Data / Performance Test ---
    print("\n--- Running Large Data Performance Test ---")

    bs_perf = BankingSystemImpl()
    num_accounts = 100000  # Large dataset size

    start_time = time.time()

    # 1. Bulk Creation
    for i in range(num_accounts):
        bs_perf.create_account(i, f"user_{i}")

    # 2. Bulk Deposit to single user
    bs_perf.deposit(num_accounts + 1, "user_0", num_accounts)

    # 3. Bulk Transfer (user_0 sends 1 unit to everyone else)
    for i in range(1, num_accounts):
        bs_perf.transfer(num_accounts + 1 + i, "user_0", f"user_{i}", 1)

    end_time = time.time()
    duration = end_time - start_time

    print(f"Performance: Processed {num_accounts * 2} operations in {duration:.4f} seconds.")

    # Verify logic holds up under load
    final_bal = bs_perf.deposit(999999, "user_0", 0)
    expect("Large Scale Logic Check (user_0 balance)", final_bal, 1)

    if duration < 2.5:
        print("PERFORMANCE STATUS: PASS (Fast)")
    else:
        print("PERFORMANCE STATUS: FAIL (Slow)")


if __name__ == "__main__":
    run_tests()