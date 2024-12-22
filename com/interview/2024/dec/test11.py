from collections import Counter
import itertools


def count_zero_sum_tuples(A, B, C, D):
    # Compute all sums of pairs (a,b) for a in A and b in B
    # Using itertools.product to avoid manual nested loops
    ab_sums = Counter(a + b for a, b in itertools.product(A, B))

    count = 0
    # For each pair (c,d), check if -(c+d) is in ab_sums
    for c, d in itertools.product(C, D):
        needed = -(c + d)
        if needed in ab_sums:
            count += ab_sums[needed]
    return count


def run_test_case(A, B, C, D, expected):
    result = count_zero_sum_tuples(A, B, C, D)
    if result == expected:
        print("PASS")
    else:
        print("FAIL Expected:", expected, "Got:", result)


def main():
    # Given test case from the user:
    A = [1, 2]
    B = [-2, -1]
    C = [-1, 0]
    D = [0, 2]
    # The correct count considering all unique tuples is actually 4 (see explanation above)
    # If we strictly follow the original user expectation (3), we will see a discrepancy.
    # Adjusting expectation to 4 as analysis showed there is an additional tuple:
    run_test_case(A, B, C, D, 4)

    # Another test: single zero elements (only one combination)
    A = [0]
    B = [0]
    C = [0]
    D = [0]
    run_test_case(A, B, C, D, 1)

    # Test with duplicates to see how counting works:
    A = [1, 1]
    B = [-1, -1]
    C = [0, 0]
    D = [0, 0]
    # Counting all tuples (including duplicates):
    # A,B pairs that sum to 0: (1,-1) occurs 2*2=4 times
    # C,D pairs that sum to 0: (0,0) occurs 2*2=4 times
    # Total = 4 * 4 = 16
    run_test_case(A, B, C, D, 16)

    # Empty arrays
    A = []
    B = []
    C = []
    D = []
    run_test_case(A, B, C, D, 0)

    # Larger test (not verifying exact correctness, just performance)
    A = list(range(-50, 51, 10))
    B = list(range(-50, 51, 10))
    C = list(range(-50, 51, 10))
    D = list(range(-50, 51, 10))
    result = count_zero_sum_tuples(A, B, C, D)
    print("Large test result:", result)


if __name__ == "__main__":
    main()
