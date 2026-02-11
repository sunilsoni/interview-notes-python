import random


def solution(numbers, pivot):
    # Count strictly greater and strictly smaller elements
    count_greater = sum(1 for x in numbers if x > pivot)
    count_less = sum(1 for x in numbers if x < pivot)

    # Compare counts and return result
    if count_greater > count_less:
        return "greater"
    elif count_less > count_greater:
        return "smaller"
    else:
        return "tie"


def run_tests():
    # Test cases from problem description
    test_cases = [
        ([1, 3, 0, -1, 1, 4, 3], 2, "smaller"),
        ([3, 4, 5, 1, 0], 3, "tie"),
        ([9, 8, -5], -1, "greater"),
        # Edge case: All equal to pivot
        ([5, 5, 5], 5, "tie"),
        # Edge case: All smaller
        ([1, 2, 3], 10, "smaller"),
        # Edge case: Single element
        ([10], 5, "greater")
    ]

    print("--- Running Standard Tests ---")
    all_passed = True
    for nums, piv, expected in test_cases:
        result = solution(nums, piv)
        status = "PASS" if result == expected else f"FAIL (Expected {expected}, got {result})"
        if status != "PASS": all_passed = False
        print(f"Input: {nums}, Pivot: {piv} -> {status}")

    # Large Data Input Test
    print("\n--- Running Large Data Test (N=1000) ---")
    large_nums = [random.randint(-1000, 1000) for _ in range(1000)]
    large_pivot = 0
    # We calculate expected strictly for validation
    exp_g = sum(1 for x in large_nums if x > large_pivot)
    exp_l = sum(1 for x in large_nums if x < large_pivot)
    expected_large = "greater" if exp_g > exp_l else "smaller" if exp_l > exp_g else "tie"

    large_result = solution(large_nums, large_pivot)
    if large_result == expected_large:
        print(f"Large Input: PASS (Length: {len(large_nums)})")
    else:
        print(f"Large Input: FAIL (Expected {expected_large}, got {large_result})")
        all_passed = False

    print("\nFinal Result:", "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED")


if __name__ == "__main__":
    run_tests()