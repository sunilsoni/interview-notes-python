from bisect import bisect_left, bisect_right
from typing import List

def findMinimumProcessDrops(starts: List[int], ends: List[int]) -> int:
    n = len(starts)
    starts_sorted = sorted(starts)
    ends_sorted = sorted(ends)
    max_overlap = 0
    for s, e in zip(starts, ends):
        # number of intervals with start <= e
        cnt_start_le = bisect_right(starts_sorted, e)
        # number of intervals with end < s
        cnt_end_lt = bisect_left(ends_sorted, s)
        overlap = cnt_start_le - cnt_end_lt
        if overlap > max_overlap:
            max_overlap = overlap
    return n - max_overlap

if __name__ == "__main__":
    test_cases = [
        # Example 1
        {"starts": [2,3,2,6,4], "ends": [3,4,4,7,6], "expected": 1},
        # Example 2
        {"starts": [1,3,4,6,9], "ends": [2,8,5,7,10], "expected": 2},
        # Single interval
        {"starts": [5], "ends": [10], "expected": 0},
        # All overlapping
        {"starts": [1,2,3], "ends": [10,9,8], "expected": 0},
        # No common overlap except one
        {"starts": [1,5,10], "ends": [2,6,11], "expected": 2},
    ]

    for i, tc in enumerate(test_cases, 1):
        result = findMinimumProcessDrops(tc["starts"], tc["ends"])
        status = "PASS" if result == tc["expected"] else "FAIL"
        print(f"Test {i}: {status} (got={result}, expected={tc['expected']})")

    # Large test for performance
    n = 200000
    large_starts = list(range(1, n+1))
    large_ends = list(range(1, n+1))
    # Expected: only one interval can overlap itself => drops = n - 1
    result = findMinimumProcessDrops(large_starts, large_ends)
    expected = n - 1
    status = "PASS" if result == expected else "FAIL"
    print(f"Large test: {status} (got={result}, expected={expected})")
