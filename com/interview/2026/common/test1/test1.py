import sys


def solve(S):
    """
    Sorts summands in a string separated by '+' in ascending order.
    """
    # Split string, sort based on integer value, join back with '+'
    return "+".join(sorted(S.split('+'), key=int))


def run_tests():
    print("--- Starting Tests ---")

    # 1. Standard cases provided in prompt
    # 2. Edge cases (single number, duplicates, multi-digit)
    test_cases = [
        ("3+2+5+1+7", "1+2+3+5+7"),
        ("9+5+4+3", "3+4+5+9"),
        ("1", "1"),
        ("1+1+1", "1+1+1"),
        ("10+2", "2+10"),  # Handles multi-digit logic
        ("0+5+0", "0+0+5")
    ]

    # 3. Large Data Input Handling
    # Generate 5000 numbers in reverse order
    large_n = 5000
    large_list = list(range(large_n, 0, -1))
    large_input = "+".join(map(str, large_list))
    # Python's Timsort is efficient (O(n log n)), handling this easily
    large_expected = "+".join(map(str, sorted(large_list)))

    test_cases.append((large_input, large_expected))
    print(f"Added large data test case (Size: {large_n} elements)")

    # Execution
    all_passed = True
    for i, (inp, expected) in enumerate(test_cases):
        try:
            result = solve(inp)
            if result == expected:
                # Truncate output for clean display if too long
                disp_res = (result[:50] + '...') if len(result) > 50 else result
                print(f"Test {i + 1}: PASS -> {disp_res}")
            else:
                print(f"Test {i + 1}: FAIL. Expected {expected[:20]}... Got {result[:20]}...")
                all_passed = False
        except Exception as e:
            print(f"Test {i + 1}: ERROR -> {e}")
            all_passed = False

    if all_passed:
        print("\nSUCCESS: All test cases passed.")
    else:
        print("\nFAILURE: Some tests failed.")


if __name__ == "__main__":
    run_tests()