def merge_intervals(intervals):
    # CASE 1: Handle None input
    if intervals is None:
        return []

    # CASE 2 & 3: Filter out None intervals and invalid values
    valid_intervals = []
    for interval in intervals:
        # Skip if interval itself is None
        if interval is None:
            continue
        # Skip if start or end is None
        if interval[0] is None or interval[1] is None:
            continue
        # Keep valid intervals
        valid_intervals.append(interval)

    # Handle empty after filtering
    if not valid_intervals:
        return []

    # Continue with normal algorithm...
    sorted_intervals = sorted(valid_intervals, key=lambda x: x[0])
    result = [sorted_intervals[0]]

    for i in range(1, len(sorted_intervals)):
        current = sorted_intervals[i]
        last = result[-1]

        if last[1] >= current[0]:
            last[1] = max(last[1], current[1])
        else:
            result.append(current)

    return result