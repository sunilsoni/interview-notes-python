def is_balanced(s: str) -> bool:
    """
    Return True if the bracket string s is balanced, else False.
    Supports (), [], {}.
    """
    # Map each closing bracket to its corresponding opening one
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = []  # will hold opening brackets

    # Iterate over each character in the input string
    for i, ch in enumerate(s):
        # If it's an opening bracket, push onto stack
        if ch in pairs.values():
            stack.append(ch)
            # Debug: print(f"Pushed {ch}, stack now: {stack}")
        # If it's a closing bracket, check for a match
        elif ch in pairs:
            # If stack empty or top doesn't match the required opening bracket
            if not stack or stack[-1] != pairs[ch]:
                # Debug: print(f"Mismatch at index {i}: expected {pairs[ch]}, found {stack[-1] if stack else None}")
                return False
            stack.pop()  # matched, so remove the opening bracket
            # Debug: print(f"Popped for {ch}, stack now: {stack}")
        else:
            # Ambiguity: character not recognized as bracket.
            # Suggestion: either ignore or treat as error.
            # For now, we'll treat any other character as invalid.
            # If you want to ignore non-brackets, comment out the next line.
            return False

    # If anything remains in stack, there are unmatched opening brackets
    return not stack


def main():
    """
    Simple test harness: reads hard-coded test cases,
    prints PASS/FAIL and handles large inputs.
    """
    test_cases = [
        ("([]){}", True),
        ("(([]",    False),
        ("",        True),
        ("[({})]",  True),
        ("[({)}]",  False),
        # add more edge cases or very long inputs:
        ("(" * 1000000 + ")" * 1000000, True),  # large balanced
    ]

    passed = 0
    for s, expected in test_cases:
        result = is_balanced(s)
        status = "PASS" if result == expected else "FAIL"
        print(f"Input: {s[:30]!r}{'...' if len(s)>30 else '':<5} "
              f"Expected: {expected}, Got: {result} → {status}")
        if status == "PASS":
            passed += 1

    print(f"\nResult: Passed {passed}/{len(test_cases)} tests.")


if __name__ == "__main__":
    main()