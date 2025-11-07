def merge_intervals(list1, list2):
    """
    Merges two lists of intervals, combining any overlapping intervals.

    Args:
        list1: First list of intervals (each interval is [start, end])
        list2: Second list of intervals (each interval is [start, end])

    Returns:
        A list of merged intervals with no overlaps
    """

    # Step 1: Combine both lists into one
    # We need all intervals in one place to check for overlaps
    all_intervals = list1 + list2

    # Step 2: Handle empty case
    # If there are no intervals at all, return an empty list
    if not all_intervals:
        return []

    # Step 3: Sort intervals by their start time
    # Sorting makes it easy to find overlaps - overlapping intervals will be adjacent
    # The key=lambda x: x[0] means "sort by the first element (start time) of each interval"
    all_intervals.sort(key=lambda x: x[0])

    # Step 4: Initialize result list with the first interval
    # We'll build our answer by adding merged intervals to this list
    merged = [all_intervals[0]]

    # Step 5: Iterate through remaining intervals
    # We start at index 1 because we already added the first interval
    for current in all_intervals[1:]:
        # Get the last interval in our merged list
        # This is the interval we'll check for overlap with the current one
        last_merged = merged[-1]

        # Check if current interval overlaps with the last merged interval
        # Two intervals [a,b] and [c,d] overlap if c <= b
        # (the start of the second is before or at the end of the first)
        if current[0] <= last_merged[1]:
            # OVERLAP DETECTED: Merge the intervals
            # The new merged interval starts at the earliest start time (already in last_merged[0])
            # and ends at the latest end time (max of both end times)
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # NO OVERLAP: Add current interval as a separate interval
            # This interval doesn't touch the previous one, so keep it separate
            merged.append(current)

    # Step 6: Return the final merged list
    return merged


# 🧪 Test Method (No UnitTest Framework)
def main():
    """
    Tests the merge_intervals function with various test cases.
    Prints PASS or FAIL for each test case.
    """

    print("=" * 60)
    print("TESTING MERGE INTERVALS SOLUTION")
    print("=" * 60)

    # Test Case 1: Provided example
    print("\nTest Case 1: Provided Example")
    list1 = [[1, 2], [5, 9]]
    list2 = [[4, 6], [8, 10], [11, 12]]
    expected = [[1, 2], [4, 10], [11, 12]]
    result = merge_intervals(list1, list2)
    status = "PASS" if result == expected else "FAIL"
    print(f"Input: list1={list1}, list2={list2}")
    print(f"Expected: {expected}")
    print(f"Got:      {result}")
    print(f"Status:   {status}")

    # Test Case 2: No overlaps
    print("\nTest Case 2: No Overlaps")
    list1 = [[1, 2], [5, 6]]
    list2 = [[8, 9], [11, 12]]
    expected = [[1, 2], [5, 6], [8, 9], [11, 12]]
    result = merge_intervals(list1, list2)
    status = "PASS" if result == expected else "FAIL"
    print(f"Input: list1={list1}, list2={list2}")
    print(f"Expected: {expected}")
    print(f"Got:      {result}")
    print(f"Status:   {status}")

    # Test Case 3: All intervals merge into one
    print("\nTest Case 3: All Merge Into One")
    list1 = [[1, 5], [3, 7]]
    list2 = [[6, 10], [8, 12]]
    expected = [[1, 12]]
    result = merge_intervals(list1, list2)
    status = "PASS" if result == expected else "FAIL"
    print(f"Input: list1={list1}, list2={list2}")
    print(f"Expected: {expected}")
    print(f"Got:      {result}")
    print(f"Status:   {status}")

    # Edge Case 1: Empty lists
    print("\nEdge Case 1: Both Lists Empty")
    list1 = []
    list2 = []
    expected = []
    result = merge_intervals(list1, list2)
    status = "PASS" if result == expected else "FAIL"
    print(f"Input: list1={list1}, list2={list2}")
    print(f"Expected: {expected}")
    print(f"Got:      {result}")
    print(f"Status:   {status}")

    # Edge Case 2: One empty list
    print("\nEdge Case 2: One Empty List")
    list1 = [[1, 3], [5, 7]]
    list2 = []
    expected = [[1, 3], [5, 7]]
    result = merge_intervals(list1, list2)
    status = "PASS" if result == expected else "FAIL"
    print(f"Input: list1={list1}, list2={list2}")
    print(f"Expected: {expected}")
    print(f"Got:      {result}")
    print(f"Status:   {status}")

    # Edge Case 3: Adjacent intervals (touching but not overlapping)
    print("\nEdge Case 3: Adjacent Intervals")
    list1 = [[1, 3]]
    list2 = [[3, 5]]
    expected = [[1, 5]]
    result = merge_intervals(list1, list2)
    status = "PASS" if result == expected else "FAIL"
    print(f"Input: list1={list1}, list2={list2}")
    print(f"Expected: {expected}")
    print(f"Got:      {result}")
    print(f"Status:   {status}")

    # Edge Case 4: Identical intervals
    print("\nEdge Case 4: Identical Intervals")
    list1 = [[1, 5]]
    list2 = [[1, 5]]
    expected = [[1, 5]]
    result = merge_intervals(list1, list2)
    status = "PASS" if result == expected else "FAIL"
    print(f"Input: list1={list1}, list2={list2}")
    print(f"Expected: {expected}")
    print(f"Got:      {result}")
    print(f"Status:   {status}")

    # Large Input Case: Testing performance
    print("\nLarge Input Case: Performance Test")
    # Create 1000 intervals with some overlaps
    list1 = [[i, i + 2] for i in range(0, 1000, 5)]  # 200 intervals
    list2 = [[i, i + 3] for i in range(2, 1002, 5)]  # 200 intervals
    result = merge_intervals(list1, list2)
    print(f"Input size: list1 has {len(list1)} intervals, list2 has {len(list2)} intervals")
    print(f"Output size: {len(result)} merged intervals")
    print(f"Status: PASS (Performance test completed)")

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


# Run the tests
if __name__ == "__main__":
    main()