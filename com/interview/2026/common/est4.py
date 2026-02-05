import collections


def solution(fragments, accessCode):
    # Convert inputs to strings for easy concatenation checks
    target = str(accessCode)
    n = len(target)

    # Count frequency of each fragment as a string
    counts = collections.Counter(map(str, fragments))
    total_ways = 0

    # Iterate through each unique fragment to find pairs
    for frag, count in counts.items():
        m = len(frag)
        # Optimization: Only check fragments shorter than the target
        if m >= n:
            continue

        # If frag is a prefix, look for the required suffix
        if target.startswith(frag):
            suffix = target[m:]
            if suffix in counts:
                # If prefix and suffix are different unique strings
                if frag != suffix:
                    total_ways += count * counts[suffix]
                # If prefix and suffix are the same, use combinations n*(n-1)
                else:
                    total_ways += count * (count - 1)

    return total_ways


def test():
    test_cases = [
        # Provided Examples
        ([1, 212, 12, 12], 1212, 3),
        ([11, 11, 110], 11011, 2),
        ([777, 7, 777, 77, 77], 7777, 6),
        # Edge Cases
        ([123, 456], 123456, 1),
        ([12, 12, 12], 1212, 6),  # 3 fragments, 3*2 combinations
        ([1, 2], 3, 0),  # No combination forms target
    ]

    for i, (frags, code, expected) in enumerate(test_cases):
        result = solution(frags, code)
        status = "PASS" if result == expected else f"FAIL (Got {result}, Expected {expected})"
        print(f"Test Case {i + 1}: {status}")


if __name__ == "__main__":
    test()