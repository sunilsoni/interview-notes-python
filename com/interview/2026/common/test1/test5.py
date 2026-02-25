def check_valid_string_stacks(s: str) -> bool:
    # A list to store the index positions of every open bracket '('
    open_stack = []

    # A list to store the index positions of every wildcard '*'
    star_stack = []

    # Loop through the string, keeping track of both the index (i) and the character (char)
    for i, char in enumerate(s):

        if char == '(':
            # We found an open bracket, so we save its exact position in the string
            open_stack.append(i)

        elif char == '*':
            # We found a star, so we save its exact position in the string
            star_stack.append(i)

        else:
            # The character must be a close bracket ')', so we need to find a match for it
            if open_stack:
                # Best case: We have an unmatched '(' waiting, so we remove its index to pair them up
                open_stack.pop()
            elif star_stack:
                # Second choice: No '(' available, so we use a '*' to act as an open bracket and remove its index
                star_stack.pop()
            else:
                # Worst case: We have a ')' but absolutely nothing to match it with, so it fails
                return False

    # Now that we've checked the whole string, let's look at any leftover '(' that didn't get closed
    while open_stack and star_stack:
        # We check if the last available '*' comes AFTER the last available '('
        if open_stack[-1] < star_stack[-1]:
            # It does! This means they form a valid pair "(*", so we remove both from our stacks
            open_stack.pop()
            star_stack.pop()
        else:
            # The '*' is BEFORE the '(', like "*(", which cannot close it. We break the loop and fail.
            break

    # If the open_stack is completely empty, it means all '(' found a valid match!
    return len(open_stack) == 0


def main():
    # We set up a list of test cases (input_string, expected_boolean_result)
    test_cases = [
        ("()", True),
        ("(*)", True),
        ("*)", True),
        ("**)", True),
        ("*))", False),
        ("(*))", True),
        ("(((******)))", True),
        ("*(", False),
    ]

    # Create a massive string for large data testing (150,000 characters total)
    large_data = "(" * 50000 + "*" * 50000 + ")" * 50000
    test_cases.append((large_data, True))

    print("--- Testing Two Stacks Approach ---")
    for i, (test_string, expected) in enumerate(test_cases, 1):
        # Call the Stacks function
        result = check_valid_string_stacks(test_string)
        # Format output so large data doesn't clutter the screen
        display_str = test_string if len(test_string) < 20 else "LARGE DATA INPUT"

        if result == expected:
            print(f"Test {i} PASS: Input '{display_str}'")
        else:
            print(f"Test {i} FAIL: Input '{display_str}'. Expected {expected}, got {result}")


if __name__ == "__main__":
    main()