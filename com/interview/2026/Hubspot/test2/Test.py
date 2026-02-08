# ==========================================
# 3. Test Runner (Updated for Level 2)
# ==========================================
def run_tests():
    bs = BankingSystemImpl()
    print("--- Running Level 2 Tests ---")

    def expect(case_name, result, expected_val):
        status = "PASS" if result == expected_val else f"FAIL\n   Got: {result}\n   Exp: {expected_val}"
        print(f"{case_name}: {status}")

    # --- Setup Accounts ---
    bs.create_account(1, "acc1")
    bs.create_account(2, "acc2")
    bs.create_account(3, "acc3")

    # --- Deposits ---
    bs.deposit(4, "acc1", 2000)
    bs.deposit(5, "acc2", 3000)
    bs.deposit(6, "acc3", 4000)

    # --- Check Initial Top Spenders (Should be all 0) ---
    # Expected: acc1(0), acc2(0), acc3(0) sorted alphabetically
    expect("Initial Spenders", bs.top_spenders(7, 3), ["acc1(0)", "acc2(0)", "acc3(0)"])

    # --- Transfers ---
    # acc3 sends 500 -> acc3 outgoing = 500
    bs.transfer(8, "acc3", "acc2", 500)

    # acc3 sends 1000 -> acc3 outgoing = 1500
    bs.transfer(9, "acc3", "acc1", 1000)

    # acc1 sends 2500 -> acc1 outgoing = 2500 (balance was 2000 + 1000 = 3000, so valid)
    bs.transfer(10, "acc1", "acc2", 2500)

    # --- Verify Top Spenders ---
    # acc1: 2500
    # acc3: 1500
    # acc2: 0
    expected_top = ["acc1(2500)", "acc3(1500)", "acc2(0)"]
    expect("Top Spenders Logic", bs.top_spenders(11, 3), expected_top)

    # --- Verify 'n' limit ---
    expect("Top Spenders Limit n=1", bs.top_spenders(12, 1), ["acc1(2500)"])

    # --- Large Data Performance Test ---
    print("\n--- Running Large Data Performance Test ---")
    bs_perf = BankingSystemImpl()
    count = 50000

    start = time.time()
    # Create accounts
    for i in range(count):
        bs_perf.create_account(i, f"u{i}")

    # User 0 sends money to everyone (Highest spender)
    bs_perf.deposit(count + 1, "u0", count * 10)
    for i in range(1, 1000):  # 1000 transfers
        bs_perf.transfer(count + 2, "u0", f"u{i}", 10)

    # Check top spenders
    res = bs_perf.top_spenders(count + 3, 5)

    duration = time.time() - start
    print(f"Result: {res}")
    print(f"Processed 50k accounts + sorts in {duration:.4f}s")

    if duration < 3.0:
        print("PERFORMANCE: PASS")
    else:
        print("PERFORMANCE: FAIL")


if __name__ == "__main__":
    run_tests()