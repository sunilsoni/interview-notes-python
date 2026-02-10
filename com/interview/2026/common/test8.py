import sys


def check_range(text, left_index, right_index):
    """
    A helper function to check if a specific section of the string is a palindrome.
    This is strict (no deletions allowed here).
    """
    # Logic: Standard palindrome check loop, but only for the given range.
    while left_index < right_index:
        if text[left_index] != text[right_index]:
            return False
        left_index += 1
        right_index -= 1
    return True


def valid_palindrome_with_deletion(input_data):
    """
    Checks if input is a palindrome, allowing at most 1 character removal.
    """

    # Logic: Handle None type safety.
    if input_data is None:
        return False

    text = str(input_data)
    left = 0
    right = len(text) - 1

    # Logic: Main loop to find the FIRST mismatch.
    while left < right:

        # Logic: If characters match, just keep shrinking the window.
        if text[left] == text[right]:
            left += 1
            right -= 1
        else:
            # --- MISMATCH FOUND ---
            # Logic: We found a bad pair. We get ONE chance to fix it.
            # We try two possibilities:

            # 1. Skip the Left character (left + 1) and check the rest.
            skip_left_result = check_range(text, left + 1, right)

            # 2. Skip the Right character (right - 1) and check the rest.
            skip_right_result = check_range(text, left, right - 1)

            # Logic: If EITHER fix works, then the string is valid.
            # Why: The problem says we can remove "at most one".
            return skip_left_result or skip_right_result

    # Logic: If we finished the loop without returning, it was a perfect palindrome.
    return True


# ---------------------------------------------------------
# 4. Testing Method
# ---------------------------------------------------------

def run_tests():
    print("--- Starting Test Execution (Deletion Allowed) ---")

    test_cases = [
        # Basic Cases
        {"input": "aba", "expected": True, "desc": "Already a palindrome"},
        {"input": "abca", "expected": True, "desc": "Remove 'c' or 'b' makes 'aba'"},
        {"input": "abc", "expected": False, "desc": "Cannot be fixed by 1 removal"},

        # Tricky Cases
        {"input": "deeee", "expected": True, "desc": "Remove 'd' -> 'eeee'"},
        {"input": "tebbem", "expected": False, "desc": "Two mismatches (t/m and b/b)"},

        # Edge Cases
        {"input": "a", "expected": True, "desc": "Single char is always valid"},
        {"input": "", "expected": True, "desc": "Empty string is valid"},
    ]

    passed_count = 0

    for i, test in enumerate(test_cases):
        input_val = test["input"]
        expected_val = test["expected"]
        desc = test["desc"]

        result = valid_palindrome_with_deletion(input_val)

        if result == expected_val:
            print(f"Test {i + 1}: PASS | {desc}")
            passed_count += 1
        else:
            print(f"Test {i + 1}: FAIL | {desc}")
            print(f"   Input: {input_val}")
            print(f"   Expected: {expected_val}, Got: {result}")

    print("-------------------------------")
    if passed_count == len(test_cases):
        print("ALL TESTS PASSED.")


if __name__ == "__main__":
    run_tests()