import sys


# 1. Solution Implementation
def getMinOperations(n):
    ops = 0
    while n > 0:
        if n & 1:  # If n is odd
            ops += 1
            # If the second bit is set (ends in 11), adding 1 reduces bits (chains carry),
            # unless n is 3 (where adding/subtracting costs same, but sub is simpler).
            # Actually for min operations of 2^i, 3->4 and 3->2 are equal cost (2).
            # We follow the standard greedy strategy for weight minimization:
            # If ends in 11 -> add 1 (propagate carry)
            # If ends in 01 -> sub 1
            if (n & 2):
                n += 1
            else:
                n -= 1
        n //= 2  # Shift right (divide by 2)
    return ops


# 2. Testing Method
def run_tests():
    print("Running Tests...")

    test_cases = [
        {"input": 21, "expected": 3},
        {"input": 5, "expected": 2},
        {"input": 7, "expected": 2},  # 7 -> 8 -> 0 (add 1, sub 8)
        {"input": 15, "expected": 2},  # 15 -> 16 -> 0
        {"input": 1, "expected": 1},
        {"input": 2, "expected": 1},
        {"input": 3, "expected": 2},
        {"input": (1 << 60) - 1, "expected": 2},  # Large Case: 2^60 - 1
        {"input": 0, "expected": 0}
    ]

    all_passed = True
    for case in test_cases:
        n = case["input"]
        expected = case["expected"]
        result = getMinOperations(n)

        status = "PASS" if result == expected else "FAIL"
        print(f"n: {n:<20} | Expected: {expected} | Got: {result} | {status}")

        if result != expected:
            all_passed = False

    # Large Data Verification
    large_input = 1234567890123456789
    print(f"\nLarge Input Check ({large_input}): {getMinOperations(large_input)} operations")

    if all_passed:
        print("\nAll Test Cases PASSED.")
    else:
        print("\nSome Test Cases FAILED.")


if __name__ == '__main__':
    # Input handling for custom testing or default test suite
    if len(sys.argv) > 1:
        # If argument provided, solve for that
        print(getMinOperations(int(sys.argv[1])))
    else:
        # Run test suite
        run_tests()