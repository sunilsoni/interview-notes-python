def valid_palindrome(s):
    def is_palindrome_range(left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left = 0
    right = len(s) - 1

    while left < right:
        if s[left] == s[right]:
            left += 1
            right -= 1
        else:
            return is_palindrome_range(left + 1, right) or is_palindrome_range(left, right - 1)

    return True


def main():
    test_cases = [
        ("tacocats", True),
        ("racecar", True),
        ("abca", True),
        ("abcdef", False),
        ("a", True),
        ("aa", True),
        ("ab", True),
        ("aba", True),
        ("abcba", True),
        ("abcde", False),
        ("raceacar", True)
    ]

    print("=" * 50)
    print("TESTING VALID PALINDROME")
    print("=" * 50)

    for i, (s, expected) in enumerate(test_cases, 1):
        result = valid_palindrome(s)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"\nTest {i}: '{s}'")
        print(f"Expected: {expected}, Got: {result} - {status}")

    print("\n" + "=" * 50)
    print("Performance Test")
    print("=" * 50)

    import time
    s = "a" * 10000 + "b" + "a" * 10000
    start = time.time()
    result = valid_palindrome(s)
    elapsed = time.time() - start
    print(f"Length: {len(s)}, Result: {result}, Time: {elapsed:.6f}s")


if __name__ == "__main__":
    main()