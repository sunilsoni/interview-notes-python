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
def run_example():
    # Example list of intervals
    intervals = [[1,3], [2,6], [8,10], [15,18]]

    # Call the merge_intervals function
    result = merge_intervals(intervals)

    # Print the output
    print("Input Intervals:", intervals)
    print("Merged Intervals:", result)


# Call the example method
run_example()
