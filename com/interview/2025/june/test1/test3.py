def is_palindrome(s: str) -> bool:
    """
    Check if s is a palindrome, ignoring non-alphanumerics and case,
    using exactly one loop (no nested loops).
    """
    left, right = 0, len(s) - 1
    comparisons = 0

    # Single loop: at each iteration we either skip left, skip right, or compare.
    while left < right:
        if not s[left].isalnum():
            # skip over non-alphanumeric on the left
            left += 1
        elif not s[right].isalnum():
            # skip over non-alphanumeric on the right
            right -= 1
        else:
            # both are alphanumeric—compare them
            comparisons += 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1

    # Only a palindrome if we did at least one comparison
    return comparisons > 0


def main():
    """
    Run test cases to verify our single-loop palindrome checker.
    """
    tests = [
        ("", True),
        ("A", True),
        ("@h@", False),                     # must be False now
        ("A?A", True),
        ("A man, a plan, a canal: Panama", True),
        ("Madam, I'm Adam.", True),
        ("No lemon, no melon!", True),
        ("Race a car", False),
        ("hello, world!", False),
    ]

    for i, (inp, exp) in enumerate(tests, 1):
        got = is_palindrome(inp)
        print(f"Test {i}: {inp!r} → expected={exp}, got={got} → {'PASS' if got==exp else 'FAIL'}")

    # Large input sanity check
    half = "Abc123!" * 200_000            # ~1.4M chars including symbols
    long_str = half + "#" + half[::-1]    # still a palindrome
    import time
    t0 = time.time()
    res = is_palindrome(long_str)
    dt = time.time() - t0
    print(f"\nLarge test (len={len(long_str):,}): result={res}, time={dt:.3f}s")


if __name__ == "__main__":
    main()