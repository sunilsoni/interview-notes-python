def check_valid_string(s: str) -> bool:
    # Keeps track of the smallest possible number of open brackets we currently have
    min_open = 0

    # Keeps track of the largest possible number of open brackets we currently have
    max_open = 0

    # Start a loop to go through each character in the string one by one
    for char in s:

        # Check if the current character is an exact open bracket
        if char == '(':
            # We must match this, so the minimum needed open brackets goes up by 1
            min_open += 1
            # It also increases the maximum possible open brackets by 1
            max_open += 1

            # Check if the current character is an exact close bracket
        elif char == ')':
            # It closes one open bracket, reducing our minimum count by 1
            min_open -= 1
            # It also reduces our maximum possible open brackets by 1
            max_open -= 1

            # If the character is neither '(' nor ')', it must be our wildcard '*'
        else:
            # The wildcard COULD act as a close bracket, reducing the minimum open count
            min_open -= 1
            # The wildcard COULD act as an open bracket, increasing the maximum open count
            max_open += 1

            # Check if even our most optimistic scenario has too many close brackets
        if max_open < 0:
            # We have unmatched close brackets that we cannot fix, so it is invalid
            return False

            # Check if our minimum open brackets dropped into negative numbers
        if min_open < 0:
            # We can't have negative brackets, so we change our mind and treat the '*' as empty, resetting to 0
            min_open = 0

            # After checking all characters, we check if it's possible to have exactly 0 open brackets left
    # If min_open is 0, we found a perfect balance and return True. Otherwise, False.
    return min_open == 0


def main():
    # List of test cases: each item is a tuple containing the input string and the expected boolean result
    test_cases = [
        ("()", True),  # Standard valid brackets
        ("(*)", True),  # Star acts as empty string
        ("*)", True),  # Star acts as open bracket
        ("**)", True),  # First star acts as open, second as empty
        ("*))", False),  # Not enough wildcards to balance the closing brackets
        ("(*, *)", False),
        # Invalid characters like comma and space will fail matching correctly, representing bad input
        ("(*))", True),  # Star acts as an open bracket to balance the extra close bracket
        ("(((******)))", True),  # Multiple wildcards acting as empty strings
        ("*(", False),  # Star cannot close an open bracket that comes after it
    ]

    # Generate a massive string for large data testing: 50,000 open brackets, 50,000 stars, 50,000 close brackets
    large_data = "(" * 50000 + "*" * 50000 + ")" * 50000
    # Add the large data test case to our list (we expect it to be True)
    test_cases.append((large_data, True))

    # Loop through each test case to run the validation
    for i, (test_string, expected) in enumerate(test_cases, 1):
        # Call our function with the test string
        result = check_valid_string(test_string)

        # Check if our function's result matches what we expect
        if result == expected:
            # If it matches, print a PASS message
            # For the large data case, we truncate the print output so it doesn't flood the console
            display_str = test_string if len(test_string) < 20 else "LARGE DATA INPUT"
            print(f"Test {i} PASS: Input '{display_str}' -> Result: {result}")
        else:
            # If it doesn't match, print a FAIL message to help with debugging
            print(f"Test {i} FAIL: Input '{test_string}'. Expected {expected}, got {result}")


# Standard Python setup to run the main method when the script is executed
if __name__ == "__main__":
    main()