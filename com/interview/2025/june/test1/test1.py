def is_palindrome(s: str) -> bool:
    """
    Return True if s is a palindrome, ignoring non-alphanumerics
    and case, and requiring at least one pair comparison
    (so that '@h@' → False).
    """
    # 1. Trivially, any string of length 0 or 1 is a palindrome.
    if len(s) < 2:
        return True

    left, right = 0, len(s) - 1
    comparisons = 0            # count how many character pairs we actually compare

    # 2. Move the two pointers inward
    while left < right:
        # skip non-alphanumeric on the left
        while left < right and not s[left].isalnum():
            left += 1
        # skip non-alphanumeric on the right
        while left < right and not s[right].isalnum():
            right -= 1

        # now both s[left] and s[right] are alphanumeric (or left >= right)
        if left < right:
            comparisons += 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1

    # 3. If we never compared any pair, it's not really a palindrome (fixes '@h@').
    return comparisons > 0


def main():
    """
    Run a suite of tests and report PASS/FAIL.
    """
    tests = [
        ("", True),
        ("A", True),
        ("@h@", False),                     # <-- now correctly False
        ("A?A", True),
        ("A man, a plan, a canal: Panama", True),
        ("Madam, I'm Adam.", True),
        ("No lemon, no melon!", True),
        ("Race a car", False),
        ("hello, world!", False),
    ]

    for i, (inp, exp) in enumerate(tests, 1):
        got = is_palindrome(inp)
        tag = "PASS" if got == exp else "FAIL"
        print(f"Test {i}: {inp!r} → expected={exp}, got={got} → {tag}")

    # Large input sanity check
    half = "Abc123!" * 200_000            # ~1.4M chars including symbols
    long_str = half + "#" + half[::-1]    # true palindrome
    import time
    t0 = time.time()
    res = is_palindrome(long_str)
    dt = time.time() - t0
    print(f"\nLarge test (len={len(long_str):,}): result={res}, time={dt:.3f}s")


if __name__ == "__main__":
    main()


def main():
    """
    Run test cases on is_palindrome(), reporting PASS/FAIL.
    Includes cases with special characters and mixed case.
    """
    test_cases = [
        ("", True),  # empty
        ("A", True),  # single letter
        ("racecar", True),  # simple palindrome
        ("Noon", True),  # mixed case
        ("hello!", False),  # punctuation non-pal
        ("A man, a plan, a canal: Panama", True),  # classic phrase
        ("Madam, I'm Adam.", True),  # another classic
        ("12321", True),  # numeric
        ("12#3 21", True),  # numbers with symbols
        ("Was it a car or a cat I saw?", True),  # question phrase
        ("Not a palindrome.", False),  # definitely not
    ]

    for idx, (input_str, expected) in enumerate(test_cases, start=1):
        result = is_palindrome(input_str)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {idx}: {input_str!r} → expected={expected}, got={result} → {status}")

    # Large-data check (still ignoring symbols)
    # construct a long palindrome with punctuation interspersed
    half = "Abc123!" * 200_000  # ~1.4 million chars including symbols
    center = "#"
    long_input = half + center + half[::-1]

    import time
    t0 = time.time()
    long_result = is_palindrome(long_input)
    dt = time.time() - t0
    print(f"\nLarge test: length={len(long_input):,}, result={long_result}, time={dt:.3f}s")


if __name__ == "__main__":
    main()