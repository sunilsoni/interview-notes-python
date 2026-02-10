import sys


def is_palindrome(input_data):
    """
    Checks if the input_data is a palindrome.
    Returns True if it is, False otherwise.
    """

    # Logic: Convert input to string just in case an integer is passed.
    # Why: We need to access characters by index (position), which we can't do with pure integers.
    text = str(input_data)

    # Logic: Initialize the 'left' pointer to the start of the string (index 0).
    # Why: We need to start checking from the very beginning.
    left_index = 0

    # Logic: Initialize the 'right' pointer to the end of the string.
    # Why: In Python, the last index is always length - 1 (because counting starts at 0).
    right_index = len(text) - 1

    # Logic: Start a loop that runs as long as the left pointer is to the left of the right pointer.
    # Why: When they cross or meet, we have checked the whole string. We don't need to check the middle twice.
    while left_index < right_index:

        # Logic: Compare the character at the left pointer with the character at the right pointer.
        # Why: This is the core rule of a palindrome. Ends must match.
        if text[left_index] != text[right_index]:
            # Logic: If they don't match, return False immediately.
            # Why: As soon as we find one mismatch, we know for sure it's not a palindrome. No need to continue.
            return False

        # Logic: Move the left pointer one step to the right.
        # Why: To check the next character in the sequence.
        left_index += 1

        # Logic: Move the right pointer one step to the left.
        # Why: To check the corresponding character from the other end.
        right_index -= 1

    # Logic: If the loop finishes without returning False, it means all characters matched.
    # Why: We survived the check! It is a palindrome.
    return True


# ---------------------------------------------------------
# 5. Testing Method (No Unit Test libraries, just pure logic)
# ---------------------------------------------------------

def run_tests():
    print("--- Starting Test Execution ---")

    # Logic: Create a list of test cases. Each case is a dictionary or tuple.
    # Why: Keeping data separate from logic makes it easy to add new tests later.
    test_cases = [
        {"input": "madam", "expected": True, "desc": "Simple odd length palindrome"},
        {"input": "radar", "expected": True, "desc": "Another simple palindrome"},
        {"input": "hello", "expected": False, "desc": "Simple non-palindrome"},
        {"input": "", "expected": True, "desc": "Empty string (Edge Case)"},
        {"input": "a", "expected": True, "desc": "Single character (Edge Case)"},
        {"input": 12321, "expected": True, "desc": "Integer Input"},
        {"input": 12345, "expected": False, "desc": "Integer Non-Palindrome"},
        {"input": "abba", "expected": True, "desc": "Even length palindrome"},
    ]

    # Logic: Add a large data test case.
    # Why: To ensure our code doesn't crash or run too slowly with big inputs.
    large_palindrome = "a" * 1000000 + "b" + "a" * 1000000
    test_cases.append({"input": large_palindrome, "expected": True, "desc": "Large Input (2 Million+ chars)"})

    # Logic: Initialize a counter for passed tests.
    passed_count = 0

    # Logic: Loop through each test case.
    for i, test in enumerate(test_cases):
        input_val = test["input"]
        expected_val = test["expected"]
        description = test["desc"]

        # Logic: Run the actual function.
        result = is_palindrome(input_val)

        # Logic: Check if the result matches expectation.
        if result == expected_val:
            print(f"Test {i + 1}: PASS | {description}")
            passed_count += 1
        else:
            print(f"Test {i + 1}: FAIL | {description}")
            print(f"   Input: {str(input_val)[:20]}...")  # Print only start of input to avoid spamming console
            print(f"   Expected: {expected_val}, Got: {result}")

    print("-------------------------------")

    # Logic: Final summary.
    if passed_count == len(test_cases):
        print("ALL TESTS PASSED SUCCESSFULLY.")
    else:
        print(f"WARNING: Only {passed_count}/{len(test_cases)} tests passed.")


# Logic: Python standard boilerplate to run the main function.
if __name__ == "__main__":
    run_tests()