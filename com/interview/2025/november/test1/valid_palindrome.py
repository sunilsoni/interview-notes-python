# Solution for: "Can the string become a palindrome by removing at most one character?"
# We'll implement an O(n) two-pointer algorithm with a small helper. Every line is commented to explain purpose.
# A simple main() runs tests (including edge cases and a large input) and prints PASS/FAIL for each case.

def valid_palindrome(s: str) -> bool:
    # Define function that returns True if s can become a palindrome after removing at most one character.
    # This uses a two-pointer scan from both ends; when a mismatch is found we try skipping one char.
    # Time: O(n), Space: O(1) auxiliary.

    # Helper: check if s[left:right+1] is a palindrome by two-pointer check.
    def is_pal_range(left: int, right: int) -> bool:
        # While left index is less than right index, compare characters and move inward.
        while left < right:
            # If characters mismatch, the substring isn't a palindrome.
            if s[left] != s[right]:
                return False
            # Move left pointer rightwards.
            left += 1
            # Move right pointer leftwards.
            right -= 1
        # If loop completes, substring is palindrome.
        return True

    # Initialize left pointer at start of string.
    left = 0
    # Initialize right pointer at end of string.
    right = len(s) - 1

    # Move pointers inward while characters match.
    while left < right:
        # If characters match, continue inward.
        if s[left] == s[right]:
            left += 1
            right -= 1
        else:
            # On first mismatch, try skipping the left character OR the right character.
            # If either resulting substring is palindrome, we can fix with 1 removal.
            return is_pal_range(left + 1, right) or is_pal_range(left, right - 1)
    # If we completed the loop without finding an unfixable mismatch, it's already OK.
    return True


# ------------------- Test harness -------------------
def main():
    # List of (input_string, expected_bool) test cases including provided example and edge cases.
    tests = [
        ("tacocats", True),  # Example from prompt: remove trailing 's' -> "tacocat" (palindrome)
        ("racecar", True),  # Already a palindrome; no removal needed
        ("abca", True),  # Remove 'c' -> "aba"
        ("abcdef", False),  # Needs more than one removal
        ("", True),  # Empty string is palindrome
        ("a", True),  # Single character
        ("ab", True),  # Remove one char yields single char -> palindrome
        ("deeee", True),  # Remove leading 'd' -> "eeee"
        ("abcda", False),  # Needs more than one removal
    ]

    # Add a large test to validate performance (200k+ characters).
    # Construct: 100k 'a', then 'b', then 'c', then 100k 'a' -> removing one char ('b' or 'c') can make it palindrome.
    n = 100_000
    large = "a" * n + "b" + "c" + "a" * n
    tests.append((large, True))

    # Keep counters for passed/failed.
    passed = 0
    failed = 0

    # Run all tests and print PASS/FAIL with expected vs actual.
    for idx, (inp, expected) in enumerate(tests, 1):
        # Execute the function on the input.
        actual = valid_palindrome(inp)
        # Compare actual with expected and print a clear result.
        if actual == expected:
            print(f"Test {idx}: PASS — input length {len(inp)} expected={expected} actual={actual}")
            passed += 1
        else:
            print(f"Test {idx}: FAIL — input length {len(inp)} expected={expected} actual={actual}")
            failed += 1

    # Summary of results.
    print(f"\nSummary: {passed} passed, {failed} failed out of {len(tests)} tests.")


# Run tests when this script is executed.
if __name__ == "__main__":
    main()
