def check_string(s: str) -> str:
    stack = []
    for ch in s:
        stack.append(ch)
        if len(stack) >= 3 and stack[-3:] == ['1', '0', '0']:
            stack.pop()
            stack.pop()
            stack.pop()
    return "yes" if not stack else "no"

# ---- Testing method ----
def main():
    test_cases = {
        ("2", "101000", "1010001"): ["yes", "no"],
        ("1", "100"): ["yes"],
        ("1", "101000"): ["yes"],
        ("1", "101"): ["no"],
        ("1", "111000"): ["no"],
        ("1", "1"): ["no"],
        ("1", "0"): ["no"],
        ("1", "100100"): ["yes"],     # 100 -> empty, 100 -> empty
        ("1", "1001001"): ["no"],     # leftover "1"
        ("1", "100" * 1000): ["yes"], # big case
    }

    for case, expected in test_cases.items():
        T = int(case[0])
        results = []
        idx = 1
        for _ in range(T):
            s = case[idx]
            idx += 1
            results.append(check_string(s))

        status = "PASS" if results == expected else "FAIL"
        print(f"Input: {case} | Expected: {expected} | Got: {results} | {status}")

if __name__ == "__main__":
    main()