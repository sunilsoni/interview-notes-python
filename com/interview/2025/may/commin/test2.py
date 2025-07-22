def is_palindrome(s: str) -> bool:
    """
    Check if the given string s is a palindrome,
    considering only alphabetic characters, ignoring case,
    spaces, digits, and punctuation.
    """

    # 1. Build a list of only the letters, all in lowercase
    filtered_chars = []
    for char in s:
        if char.isalpha():                # keep only letters
            filtered_chars.append(char.lower())

    # 2. Use two pointers to compare characters from both ends
    left, right = 0, len(filtered_chars) - 1
    while left < right:
        if filtered_chars[left] != filtered_chars[right]:
            return False                  # mismatch → not a palindrome
        left += 1                         # move inward from left
        right -= 1                        # move inward from right

    return True                           # all matched → palindrome


if __name__ == "__main__":
    # Test cases: input → expected output
    test_cases = {
        "lasdlfjasldf": False,
        "racecar":       True,
        "RaceCar":       True,
        "A man, a plan, a canal: Panama": True,
        "":              True,   # empty string
        "!!!":           True,   # only punctuation
        "12321":         True,   # digits are ignored → empty → True
        "No 'x' in Nixon": True, # mixed case & punctuation
    }

    # 3. Run and print PASS/FAIL for each test
    for inp, expected in test_cases.items():
        result = is_palindrome(inp)
        status = "PASS" if result == expected else "FAIL"
        print(f"Input: {inp!r:30} → Expected: {expected}, Got: {result} → {status}")

    # 4. Large‐data sanity check (e.g., 1 million 'a's)
    large_input = "A" * 1_000_000
    print("\nLarge input test:",
          "PASS" if is_palindrome(large_input) else "FAIL")