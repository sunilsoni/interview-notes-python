"""

**Problem:**

In a typing practice application, you need to validate the consistency of user input. Given a string `typedText` that includes uppercase and lowercase English letters, you need to compute the difference between the number of uppercase and lowercase letters in this string. Return the difference as an integer.

**Note:** You are not expected to provide the most optimal solution, but a solution with time complexity not worse than `O(typedText.length^2)` will fit within the execution time limit.

---

**Example:**

1. For `typedText = "CodeSignal"`, the output should be `solution(typedText) = -6`.

    - **Explanation:**
      - There are 2 uppercase letters ('C', 'S') and 8 lowercase letters ('o', 'd', 'e', 'i', 'g', 'n', 'a', 'l').
      - The difference is `2 - 8 = -6`.

2. For `typedText = "a"`, the output should be `solution(typedText) = -1`.

    - **Explanation:**
      - There are no uppercase letters and 1 lowercase letter ('a').
      - The difference is `0 - 1 = -1`.

3. For `typedText = "AbCdEf"`, the output should be `solution(typedText) = 0`.

    - **Explanation:**
      - There are 3 uppercase letters ('A', 'C', 'E') and 3 lowercase letters ('b', 'd', 'f').
      - The difference is `3 - 3 = 0`.

---

**Input/Output:**

- **[execution time limit]** 4 seconds (py3)
- **[memory limit]** 1 GB
- **[input]** string `typedText`: A string consisting of uppercase and lowercase English letters.
    - **Guaranteed constraints:** `0 ≤ typedText.length ≤ 100`.
- **[output]** integer: The difference between the number of uppercase and lowercase letters in the input string.

---"""

def solution(typedText):
    """
    Computes the difference between the number of uppercase and lowercase letters in the input string.

    Args:
    typedText (str): The string to analyze.

    Returns:
    int: The difference (number of uppercase letters minus number of lowercase letters).
    """
    uppercase_count = sum(1 for char in typedText if char.isupper())
    lowercase_count = sum(1 for char in typedText if char.islower())
    return uppercase_count - lowercase_count


if __name__ == "__main__":
    # List of test cases as dictionaries with 'input' and 'expected' keys.
    tests = [
        {"input": "CodeSignal", "expected": -6},
        {"input": "a", "expected": -1},
        {"input": "AbCdEf", "expected": 0},
        {"input": "", "expected": 0},  # Edge case: empty string.
        {"input": "ABC", "expected": 3},  # All uppercase.
        {"input": "abc", "expected": -3},  # All lowercase.
        {"input": "AaAaBbBb", "expected": 0}  # Mixed equal counts.
    ]

    # Testing each test case.
    all_passed = True
    for test in tests:
        result = solution(test["input"])
        if result == test["expected"]:
            print(f"PASS: Input: {test['input']!r} => Output: {result}, Expected: {test['expected']}")
        else:
            print(f"FAIL: Input: {test['input']!r} => Output: {result}, Expected: {test['expected']}")
            all_passed = False

    # Testing with large data input to ensure performance.
    # Construct a string with 100 characters alternating uppercase and lowercase.
    large_input = "".join("A" if i % 2 == 0 else "a" for i in range(100))
    expected_large_result = 50 - 50  # 50 uppercase and 50 lowercase
    large_result = solution(large_input)
    if large_result == expected_large_result:
        print(f"PASS: Large Input Test => Output: {large_result}, Expected: {expected_large_result}")
    else:
        print(f"FAIL: Large Input Test => Output: {large_result}, Expected: {expected_large_result}")
        all_passed = False

    if all_passed:
        print("All test cases passed!")
    else:
        print("Some test cases failed.")