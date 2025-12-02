# Python 3 implementation for "Merge Overlapping Intervals"

from typing import List  # We import List for type hints to make code easier to read


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge overlapping intervals.

    :param intervals: List of [start, end] pairs.
    :return: New list of merged, non-overlapping intervals sorted by start.
    """
    # First, we handle a simple edge case: if the input list is empty.
    if not intervals:  # If there are no intervals at all
        return []      # we immediately return an empty list because there is nothing to merge.

    # We sort the intervals by their start value so that potential overlaps are next to each other.
    # key=lambda x: x[0] means "sort by the first element of each [start, end] pair".
    intervals.sort(key=lambda x: x[0])

    # We will build our result in this list.
    # It will hold merged intervals that are guaranteed to be non-overlapping.
    merged: List[List[int]] = []

    # We take the first interval as the initial "current" interval to compare others with.
    current_start, current_end = intervals[0]  # Unpack the first interval into start and end

    # Now we loop over the remaining intervals one by one (we skip the first because we already used it).
    for start, end in intervals[1:]:
        # For each new interval [start, end], we check if it overlaps with our current interval.
        # Overlap (or touching) happens when the new start is <= current_end.
        if start <= current_end:
            # If they overlap or touch, we need to merge them.
            # The new merged interval will start at current_start
            # and end at the maximum of current_end and the new end.
            if end > current_end:      # If the new interval extends further to the right
                current_end = end      # we update current_end to cover this larger range.
            # If end <= current_end, we do nothing because the current interval already covers it.
        else:
            # If start > current_end, there is no overlap with the current interval.
            # That means the current interval is finished and can be safely added to the result.
            merged.append([current_start, current_end])  # Add the completed interval to merged list.

            # Now we start a new current interval with [start, end].
            current_start, current_end = start, end      # Reset current_start and current_end.

    # After we finish the loop, we still have one last interval in [current_start, current_end]
    # that has not yet been added to the result.
    merged.append([current_start, current_end])  # Add this final interval.

    # Finally, we return the list of merged, non-overlapping intervals.
    return merged


def run_all_tests() -> None:
    """
    Simple manual test runner using a main-style function.
    It prints PASS/FAIL for each test case and also includes a large-data test.
    """
    # We create a list of dictionaries, where each dictionary represents one test case.
    tests = [
        # Test case 1: example from the question where there are partial overlaps.
        {
            "name": "Example 1 - simple overlaps",
            "intervals": [[1, 3], [2, 6], [8, 10], [15, 18]],
            "expected": [[1, 6], [8, 10], [15, 18]],
        },
        # Test case 2: example where intervals touch at the boundary (4 == 4).
        {
            "name": "Example 2 - touching endpoints",
            "intervals": [[1, 4], [4, 5]],
            "expected": [[1, 5]],
        },
        # Test case 3: empty input should return empty output.
        {
            "name": "Empty list",
            "intervals": [],
            "expected": [],
        },
        # Test case 4: single interval should be returned as-is.
        {
            "name": "Single interval",
            "intervals": [[5, 7]],
            "expected": [[5, 7]],
        },
        # Test case 5: already non-overlapping and sorted intervals.
        {
            "name": "Already disjoint",
            "intervals": [[1, 2], [3, 4], [5, 6]],
            "expected": [[1, 2], [3, 4], [5, 6]],
        },
        # Test case 6: intervals completely inside a larger interval.
        {
            "name": "Nested intervals",
            "intervals": [[1, 10], [2, 3], [4, 8]],
            "expected": [[1, 10]],
        },
        # Test case 7: intervals are unsorted; we check that sorting + merge works.
        {
            "name": "Unsorted input",
            "intervals": [[5, 6], [1, 2], [2, 4]],
            "expected": [[1, 4], [5, 6]],
        },
    ]

    # Now we add a large-data test case to check performance and stability.
    # We create many overlapping intervals so they should merge into one big interval.
    # Example: [0,2], [1,3], [2,4], ... up to [99999, 100001]
    large_intervals = [[i, i + 2] for i in range(0, 100000)]  # 100,000 intervals with heavy overlap

    # The first interval starts at 0, and the last interval ends at 100001,
    # and since they all chain-overlap, the merged result should be [[0, 100001]].
    tests.append(
        {
            "name": "Large overlapping chain (performance test)",
            "intervals": large_intervals,
            "expected": [[0, 100001]],
        }
    )

    # Now we run through each test, call merge_intervals, and compare with expected.
    for index, test in enumerate(tests, start=1):
        # We copy intervals so that if our function accidentally modifies them,
        # it does not affect the original test data (good testing practice).
        input_copy = [interval[:] for interval in test["intervals"]]

        # We call our merge function to get the actual result.
        actual = merge_intervals(input_copy)

        # We check if the actual result matches the expected result exactly.
        if actual == test["expected"]:
            # If they match, we print PASS with the test name.
            print(f"Test {index} - {test['name']}: PASS")
        else:
            # If they do not match, we print FAIL and show a small summary.
            print(f"Test {index} - {test['name']}: FAIL")
            print(f"  Input (first few): {test['intervals'][:10]}{' ...' if len(test['intervals']) > 10 else ''}")
            print(f"  Expected:         {test['expected']}")
            print(f"  Actual (first few): {actual[:10]}{' ...' if len(actual) > 10 else ''}")


# Standard Python pattern to run tests when this file is executed directly.
if __name__ == "__main__":
    # When you run this file with "python3 filename.py", this block will run,
    # and it will execute all our test cases and print PASS/FAIL.
    run_all_tests()
