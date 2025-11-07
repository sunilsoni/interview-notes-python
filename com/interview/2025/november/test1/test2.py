def remove_duplicates(s):
    stack = []

    for char in s:
        if stack and stack[-1] == char:
            stack.pop()
        else:
            stack.append(char)

    return ''.join(stack)


def main():
    test_cases = [
        ("abbba", "aba"),
        ("abba", ""),
        ("aabbcc", ""),
        ("aabbc", "c"),
        ("a", "a"),
        ("", ""),
        ("abcde", "abcde"),
        ("aabbccdd", ""),
        ("aabbbccc", "abc"),
        ("azxxzy", "ay"),
        ("aaaaa", "a"),
        ("aaaaaa", ""),
    ]

    print("=" * 60)
    print("TESTING REMOVE ADJACENT DUPLICATES")
    print("=" * 60)

    all_pass = True
    for i, (input_str, expected) in enumerate(test_cases, 1):
        result = remove_duplicates(input_str)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        if result != expected:
            all_pass = False

        print(f"\nTest {i}:")
        print(f"  Input:    '{input_str}'")
        print(f"  Expected: '{expected}'")
        print(f"  Got:      '{result}'")
        print(f"  {status}")

    print("\n" + "=" * 60)
    print("Performance Test")
    print("=" * 60)

    import time
    s = "ab" * 50000
    start = time.time()
    result = remove_duplicates(s)
    elapsed = time.time() - start
    print(f"Input length: {len(s)}")
    print(f"Output length: {len(result)}")
    print(f"Time: {elapsed:.6f}s")

    print("\n" + "=" * 60)
    if all_pass:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)


if __name__ == "__main__":
    main()