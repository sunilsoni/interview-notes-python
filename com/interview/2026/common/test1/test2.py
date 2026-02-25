def is_valid_bracket_string(s: str) -> bool:
    # We create a dictionary to map each closing bracket to its correct opening bracket
    bracket_map = {')': '(', '}': '{', ']': '['}

    # We initialize an empty list named 'stack' to keep track of our opening brackets
    stack = []

    # We start a loop to look at every single character in our input string 's'
    for char in s:
        # We check if the current character is a closing bracket by checking if it is a key in our dictionary
        if char in bracket_map:
            # We grab the top bracket from the stack if the stack has items, otherwise we assign a dummy '#'
            top_element = stack.pop() if stack else '#'

            # We compare the correct opening bracket (from our map) with the one we popped from the stack
            if bracket_map[char] != top_element:
                # If they do not match, it means the brackets are out of order or mismatched, so we return False
                return False

        # If the character is not a closing bracket, it must be an opening bracket
        else:
            # We push this opening bracket onto our stack so we can try to match it later
            stack.append(char)

    # If the stack is completely empty at the end, it means every open bracket found a match; return True if so, False otherwise
    return not stack


def main():
    # We define a list of test cases, each containing the input string and the expected boolean result
    test_cases = [
        # Basic valid case with one type of bracket
        ("()", True),
        # Valid case with multiple types of brackets in sequence
        ("()[]{}", True),
        # Valid case with nested brackets
        ("{[()]}", True),
        # Invalid case with wrong closing bracket
        ("(]", False),
        # Invalid case where order is crossed
        ("([)]", False),
        # Invalid case with only opening brackets
        ("((", False),
        # Invalid case with only closing brackets
        ("))", False),
        # Empty string case (valid as there are no mismatches)
        ("", True),
        # Large data case: 50,000 open parentheses followed by 50,000 close parentheses
        ("(" * 50000 + ")" * 50000, True),
        # Large data case: 50,000 pairs but ending with an invalid mismatch
        ("(" * 50000 + ")" * 49999 + "]", False)
    ]

    # We loop through our defined test cases to run them one by one
    for i, (input_str, expected) in enumerate(test_cases):
        # We call our function with the current test string
        result = is_valid_bracket_string(input_str)

        # We check if our function's result matches the expected result to determine PASS or FAIL
        status = "PASS" if result == expected else "FAIL"

        # To avoid printing 100,000 characters to the console, we truncate large strings for display purposes
        display_str = input_str if len(input_str) < 20 else input_str[:10] + "..." + input_str[-10:]

        # We print out the test number, the truncated input, the expected result, the actual result, and the PASS/FAIL status
        print(
            f"Test {i + 1}: Input: '{display_str:<20}' | Expected: {str(expected):<5} | Got: {str(result):<5} -> {status}")


# We check if this file is being run directly as a script
if __name__ == "__main__":
    # We execute the main testing function
    main()