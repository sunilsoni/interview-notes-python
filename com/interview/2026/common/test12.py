def make_valid_string(s):
    # We turn the string into a list because we can't change strings directly in Python
    # This makes it easy to skip characters we want to 'delete' later
    char_list = list(s)

    # This stack will keep track of the position (index) of '(' characters
    # If we find a ')', we will pop from here to create a pair
    stack = []

    # We use a set to store the index of every character that is NOT balanced
    # Sets are very fast for checking 'is this index here?' later on
    to_remove = set()

    # Loop through every character in the input string one by one
    for index, char in enumerate(char_list):
        if char == '(':
            # We found an opening bracket. We save its index in the stack.
            # We don't know if it's valid yet; it needs a matching ')' later.
            stack.append(index)

        elif char == ')':
            # We found a closing bracket. Let's see if there is a '(' to match it.
            if stack:
                # There is an index in the stack! We found a pair, so we pop it.
                # This '(' is now considered 'balanced'.
                stack.pop()
            else:
                # The stack is empty, meaning this ')' has no '(' before it.
                # It is invalid, so we mark its index for removal.
                to_remove.add(index)

    # After the loop, if there are still indexes left in the stack,
    # those are '(' that never found a closing ')'. They must be removed.
    while stack:
        to_remove.add(stack.pop())

    # Now we build the final string using only the characters NOT marked for removal
    result = []
    for index, char in enumerate(char_list):
        # If the current index is NOT in our 'to_remove' set, we keep it
        if index not in to_remove:
            result.append(char)

    # Combine the list of characters back into one single string
    return "".join(result)


# --- TESTING SECTION ---
def test_solution():
    # Test cases provided in the image and additional edge cases
    test_data = [
        ("(((((", ""),  # All removed
        ("(()()(", "()()"),  # Prune start/end
        (")()())", "()()"),  # Prune start/end
        ("lee(t(c)o)de)", "lee(t(c)o)de"),  # Standard case
        ("a)b(c)d", "ab(c)d"),  # Single middle removal
        ("123", "123"),  # No parentheses
        ("", ""),  # Empty input
    ]

    print(f"{'INPUT':<15} | {'EXPECTED':<15} | {'RESULT':<15} | {'STATUS'}")
    print("-" * 65)

    for inp, expected in test_data:
        actual = make_valid_string(inp)
        status = "PASS" if actual == expected else "FAIL"
        print(f"{inp:<15} | {expected:<15} | {actual:<15} | {status}")


# Execute tests
if __name__ == "__main__":
    test_solution()