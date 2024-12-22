def count_zero_sum_tuples(A, B, C, D):
    pair_sums = {}

    # Compute sums of all pairs from A and B
    for a in A:
        for b in B:
            s = a + b
            pair_sums[s] = pair_sums.get(s, 0) + 1

    # Count tuples that sum to zero
    count = 0
    for c in C:
        for d in D:
            needed = -(c + d)
            if needed in pair_sums:
                count += pair_sums[needed]

    return count


def run_test_case(A, B, C, D, expected):
    result = count_zero_sum_tuples(A, B, C, D)
    if result == expected:
        print("PASS")
    else:
        print("FAIL", "Expected:", expected, "Got:", result)


def main():
    # Provided test case
    A = [1, 2]
    B = [-2, -1]
    C = [-1, 0]
    D = [0, 2]
    # Expected result: 3
    run_test_case(A, B, C, D, 3)

    # Additional test cases:
    # Edge case 1: all arrays empty
    A = []
    B = []
    C = []
    D = []
    # No tuples possible
    run_test_case(A, B, C, D, 0)

    # Edge case 2: single elements that sum to zero
    A = [0]
    B = [0]
    C = [0]
    D = [0]
    # Only one tuple (0,0,0,0)
    run_test_case(A, B, C, D, 1)

    # Test with duplicates
    A = [1, 1]
    B = [-1, -1]
    C = [0, 0]
    D = [0, 0]
    # (1, -1, 0, 0) appears multiple times due to duplicates
    # A and B pairs: (1,-1), (1,-1) - 2 occurrences
    # C and D pairs: (0,0), (0,0) - 2 occurrences
    # Total: 2 * 2 = 4
    run_test_case(A, B, C, D, 4)

    # Large data test (just a sanity check; might not print actual PASS/FAIL)
    # Not huge data here, but bigger than above:
    A = [i for i in range(-50, 51, 10)]
    B = [i for i in range(-50, 51, 10)]
    C = [i for i in range(-50, 51, 10)]
    D = [i for i in range(-50, 51, 10)]
    # We won't have an expected value easily, just run to ensure performance.
    result = count_zero_sum_tuples(A, B, C, D)
    print("Large test result (not verifying pass/fail):", result)


if __name__ == "__main__":
    main()
