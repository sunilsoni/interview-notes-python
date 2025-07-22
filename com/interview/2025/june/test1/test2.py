def is_palindrome(s: str) -> bool:
    """
    Check if the given string s is a palindrome.

    Args:
        s (str): The input string to check.

    Returns:
        bool: True if s is a palindrome, False otherwise.
    """
    left = 0  # Start pointer at beginning of string
    right = len(s) - 1  # Start pointer at end of string

    # Move pointers toward the center
    while left < right:
        if s[left] != s[right]:
            # Mismatch found: not a palindrome
            return False
        left += 1  # Move left pointer one step right
        right -= 1  # Move right pointer one step left

    # All character pairs matched
    return True


def main():
    """
    Run a suite of test cases on is_palindrome() and report PASS/FAIL.
    Also demonstrate performance on a large input.
    """
    test_cases = [
        ("", True),  # empty string
        ("a", True),  # single char
        ("racecar", True),  # odd-length palindrome
        ("noon", True),  # even-length palindrome
        ("hello", False),  # non-palindrome
        ("RaceCar", False),  # case-sensitive check
        ("12321", True),  # numeric palindrome
        ("123210", False),  # numeric non-palindrome
    ]

    # Run each test
    for idx, (input_str, expected) in enumerate(test_cases, start=1):
        result = is_palindrome(input_str)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {idx}: is_palindrome({input_str!r}) == {expected} → {status}")

    # Large input test
    large_half = "a" * 1_000_000  # one million 'a's
    large_input = large_half + "b" + large_half  # 2M+1 length, not a palindrome
    # We expect False
    import time
    start = time.time()
    large_result = is_palindrome(large_input)
    duration = time.time() - start
    print(f"\nLarge input test (length={len(large_input)}): result={large_result}, time={duration:.3f}s")


if __name__ == "__main__":
    main()