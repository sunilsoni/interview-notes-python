def isValid(s: str) -> bool:
    # Initialize stack to store opening brackets
    stack = []

    # Dictionary to map closing brackets to their corresponding opening brackets
    brackets_map = {
        ')': '(',
        '}': '{',
        ']': '['
    }

    # Iterate through each character in the string
    for char in s:
        # If it's a closing bracket
        if char in brackets_map:
            # Pop the top element if stack is not empty, else assign dummy value
            top_element = stack.pop() if stack else '#'

            # Check if the popped element matches the corresponding opening bracket
            if brackets_map[char] != top_element:
                return False
        else:
            # If it's an opening bracket, push to stack
            stack.append(char)

    # Return true if stack is empty (all brackets matched)
    return len(stack) == 0


def test_bracket_validator():
    # Test cases with expected results
    test_cases = [
        ("()", True),  # Basic valid case
        ("()[]{}", True),  # Multiple valid brackets
        ("(]", False),  # Mismatched brackets
        ("([)]", False),  # Incorrect order
        ("{[]}", True),  # Nested brackets
        ("", True),  # Empty string
        ("(", False),  # Incomplete brackets
        (")", False),  # Only closing bracket
        ("((()))", True),  # Multiple nested brackets
        ("((())", False),  # Incomplete nested brackets
        ("{[()]}", True),  # Complex nested brackets
        ("([{}])", True),  # Complex valid arrangement
        ("([{]})", False),  # Complex invalid arrangement
        ("(" * 10000 + ")" * 10000, True),  # Large input - valid
        ("(" * 10000 + ")" * 9999, False)  # Large input - invalid
    ]

    # Run tests and print results
    for i, (test_input, expected) in enumerate(test_cases, 1):
        result = isValid(test_input)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i}: Input='{test_input[:50]}{'...' if len(test_input) > 50 else ''}' "
              f"Expected={expected} Got={result} -> {status}")


# Run the tests
if __name__ == "__main__":
    test_bracket_validator()
