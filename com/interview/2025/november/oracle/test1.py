def merge_intervals(intervals):
    """
    Merges all overlapping intervals into non-overlapping intervals.

    What is an interval?
    - An interval is a range with start and end points
    - Example: [1, 3] means range from 1 to 3

    What is overlapping?
    - Two intervals overlap when one starts before the other ends
    - Example: [1,3] and [2,6] overlap because 2 <= 3
    """

    # ============================================================
    # STEP 1: Handle edge cases (empty or single interval)
    # ============================================================

    # Check if input list is empty or has no intervals
    # Why? If empty, nothing to merge, return empty list
    if not intervals:
        return []  # Return empty list for empty input

    # Check if only one interval exists
    # Why? Single interval cannot overlap with anything
    if len(intervals) == 1:
        return intervals  # Return as-is, no merging needed

    # ============================================================
    # STEP 2: Sort intervals by their start time
    # ============================================================

    # Sort all intervals based on the first element (start time)
    # Why sorting? To process intervals in order, so we can compare neighbors
    #
    # Example: [[8,10], [1,3], [2,6]]
    # After sort: [[1,3], [2,6], [8,10]]
    #
    # key=lambda x: x[0] means:
    #   - lambda creates a small function
    #   - x is each interval
    #   - x[0] is the start time of that interval
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    # ============================================================
    # STEP 3: Initialize result list with first interval
    # ============================================================

    # Create result list to store merged intervals
    # Start with the first sorted interval
    # Why? We need something to compare the next intervals against
    merged_result = [sorted_intervals[0]]

    # ============================================================
    # STEP 4: Process each remaining interval one by one
    # ============================================================

    # Loop through all intervals starting from index 1 (second interval)
    # Why start from 1? First interval (index 0) is already in result
    for i in range(1, len(sorted_intervals)):

        # Get the current interval we are processing
        # current_interval[0] = start time
        # current_interval[1] = end time
        current_interval = sorted_intervals[i]

        # Get the last interval in our merged result list
        # This is what we compare against to check for overlap
        # Why last interval? Because intervals are sorted, overlaps happen with previous
        last_merged_interval = merged_result[-1]

        # ============================================================
        # STEP 5: Check if current interval overlaps with last merged
        # ============================================================

        # Two intervals overlap when:
        # - The end of previous interval >= start of current interval
        #
        # Example of OVERLAP:
        #   last_merged = [1, 3], current = [2, 6]
        #   3 >= 2 is TRUE, so they overlap
        #   Merged becomes [1, 6]
        #
        # Example of NO OVERLAP:
        #   last_merged = [1, 3], current = [8, 10]
        #   3 >= 8 is FALSE, so they don't overlap

        # Extract start and end times for easy reading
        current_start = current_interval[0]  # Start of current interval
        current_end = current_interval[1]  # End of current interval
        last_end = last_merged_interval[1]  # End of last merged interval

        # Check if there is an overlap
        if last_end >= current_start:
            # ============================================================
            # OVERLAP FOUND: Merge by extending the end time
            # ============================================================

            # When overlapping, we extend the end of last merged interval
            # Take the maximum of both end times
            # Why max? The merged interval should cover both original intervals
            #
            # Example:
            #   last = [1, 3], current = [2, 6]
            #   max(3, 6) = 6
            #   Result: [1, 6]
            #
            # Another Example (current completely inside last):
            #   last = [1, 10], current = [2, 5]
            #   max(10, 5) = 10
            #   Result: [1, 10] (stays same)

            merged_result[-1][1] = max(last_end, current_end)

        else:
            # ============================================================
            # NO OVERLAP: Add current interval as new separate interval
            # ============================================================

            # No overlap means there is a gap between intervals
            # So we add current interval as a new entry in result
            #
            # Example:
            #   last = [1, 3], current = [8, 10]
            #   3 < 8, no overlap
            #   Result list becomes: [[1,3], [8,10]]

            merged_result.append(current_interval)

    # ============================================================
    # STEP 6: Return the final merged intervals
    # ============================================================

    # Return the list containing all merged non-overlapping intervals
    return merged_result


def run_all_tests():
    """
    Test function to verify the merge_intervals function works correctly.
    Tests various cases including edge cases and large data.
    """

    # ============================================================
    # Define all test cases
    # ============================================================

    # Each test case is a dictionary with:
    # - 'name': description of what we're testing
    # - 'input': the intervals to merge
    # - 'expected': what the output should be

    test_cases = [
        # ----------------------------------------------------------
        # Basic test cases from problem statement
        # ----------------------------------------------------------
        {
            'name': 'Example 1: Basic overlapping intervals',
            'input': [[1, 3], [2, 6], [8, 10], [15, 18]],
            'expected': [[1, 6], [8, 10], [15, 18]]
            # [1,3] and [2,6] overlap -> merge to [1,6]
            # [8,10] and [15,18] don't overlap -> stay separate
        },
        {
            'name': 'Example 2: Adjacent intervals (touching at boundary)',
            'input': [[1, 4], [4, 5]],
            'expected': [[1, 5]]
            # [1,4] and [4,5] touch at 4 -> considered overlapping
        },

        # ----------------------------------------------------------
        # Edge cases
        # ----------------------------------------------------------
        {
            'name': 'Edge Case: Empty input',
            'input': [],
            'expected': []
            # Empty list should return empty list
        },
        {
            'name': 'Edge Case: Single interval',
            'input': [[5, 10]],
            'expected': [[5, 10]]
            # Single interval has nothing to merge with
        },
        {
            'name': 'Edge Case: No overlapping intervals',
            'input': [[1, 2], [4, 5], [7, 8]],
            'expected': [[1, 2], [4, 5], [7, 8]]
            # All intervals have gaps, no merging needed
        },
        {
            'name': 'Edge Case: All intervals merge into one',
            'input': [[1, 5], [2, 6], [3, 7], [4, 8]],
            'expected': [[1, 8]]
            # All intervals overlap with each other
        },
        {
            'name': 'Edge Case: Unsorted input',
            'input': [[8, 10], [1, 3], [2, 6], [15, 18]],
            'expected': [[1, 6], [8, 10], [15, 18]]
            # Same as Example 1 but input is not sorted
        },
        {
            'name': 'Edge Case: One interval inside another',
            'input': [[1, 10], [3, 5], [4, 6]],
            'expected': [[1, 10]]
            # [3,5] and [4,6] are completely inside [1,10]
        },
        {
            'name': 'Edge Case: Same start different end',
            'input': [[1, 4], [1, 5], [1, 3]],
            'expected': [[1, 5]]
            # All start at 1, take the maximum end
        },
        {
            'name': 'Edge Case: Identical intervals',
            'input': [[2, 5], [2, 5], [2, 5]],
            'expected': [[2, 5]]
            # All same, merge into one
        },
        {
            'name': 'Edge Case: Negative numbers',
            'input': [[-10, -5], [-7, -3], [0, 5]],
            'expected': [[-10, -3], [0, 5]]
            # Should work with negative numbers too
        },

        # ----------------------------------------------------------
        # Large data test case
        # ----------------------------------------------------------
        {
            'name': 'Large Data: Many intervals (performance test)',
            'input': [[i, i + 2] for i in range(0, 10000, 1)],
            # Creates: [[0,2], [1,3], [2,4], ..., [9999,10001]]
            # All overlap because each [i, i+2] overlaps with [i+1, i+3]
            'expected': [[0, 10001]]
            # All merge into one big interval
        },
        {
            'name': 'Large Data: No overlaps (performance test)',
            'input': [[i * 10, i * 10 + 5] for i in range(1000)],
            # Creates: [[0,5], [10,15], [20,25], ..., [9990, 9995]]
            # None overlap because gaps of 5 between each
            'expected': [[i * 10, i * 10 + 5] for i in range(1000)]
            # All stay separate
        },
    ]

    # ============================================================
    # Run each test case and check results
    # ============================================================

    # Track how many tests passed
    passed_count = 0
    failed_count = 0

    # Print header
    print("=" * 70)
    print("RUNNING ALL TEST CASES")
    print("=" * 70)
    print()

    # Loop through each test case
    for test_number, test_case in enumerate(test_cases, start=1):

        # Extract test case details
        test_name = test_case['name']
        test_input = test_case['input']
        expected_output = test_case['expected']

        # Make a copy of input because sorting might modify it
        # Why copy? To preserve original input for display
        input_copy = [interval[:] for interval in test_input]

        # Run the merge function
        actual_output = merge_intervals(input_copy)

        # Check if output matches expected
        test_passed = actual_output == expected_output

        # Update counters
        if test_passed:
            passed_count += 1
            status = "✓ PASS"
        else:
            failed_count += 1
            status = "✗ FAIL"

        # Print test result
        print(f"Test {test_number}: {status}")
        print(f"  Name: {test_name}")

        # For large data, don't print full arrays
        if len(test_input) > 10:
            print(f"  Input: [{len(test_input)} intervals] (too large to display)")
            print(f"  Expected: [{len(expected_output)} intervals]")
            print(f"  Actual: [{len(actual_output)} intervals]")
        else:
            print(f"  Input: {test_input}")
            print(f"  Expected: {expected_output}")
            print(f"  Actual: {actual_output}")

        print()

    # ============================================================
    # Print final summary
    # ============================================================

    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {len(test_cases)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")

    if failed_count == 0:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print(f"\n⚠️  {failed_count} TEST(S) FAILED - Please review the failing cases")

    print("=" * 70)

    # Return True if all tests passed, False otherwise
    return failed_count == 0


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    """
    Main entry point of the program.
    This runs when you execute the script directly.
    """

    # Run all test cases
    all_passed = run_all_tests()

    # Exit with appropriate code
    # 0 = success (all tests passed)
    # 1 = failure (some tests failed)
    if all_passed:
        exit(0)
    else:
        exit(1)