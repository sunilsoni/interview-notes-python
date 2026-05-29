from typing import List


def fountainActivation(locations: List[int]) -> int:
    # Store total number of garden positions.
    n = len(locations)

    # If there are no positions, no fountain is needed.
    if n == 0:
        return 0

    # max_reach_from_start[left] will store the farthest right position
    # reachable by any fountain whose coverage starts at position left.
    # We use n + 1 size because garden positions are 1-based.
    max_reach_from_start = [0] * (n + 1)

    # Go through each fountain.
    for index, radius in enumerate(locations):

        # Convert 0-based Python index to 1-based garden position.
        position = index + 1

        # Calculate left coverage boundary.
        # max is used so fountain does not go before position 1.
        left = max(1, position - radius)

        # Calculate right coverage boundary.
        # min is used so fountain does not go beyond position n.
        right = min(n, position + radius)

        # For this left boundary, store the farthest right coverage.
        # If multiple fountains start from same left, keep the best one.
        max_reach_from_start[left] = max(max_reach_from_start[left], right)

    # fountains_count stores how many fountains we activate.
    fountains_count = 0

    # current_end means all positions up to this point are covered
    # using the fountains selected so far.
    current_end = 0

    # farthest_reach means the farthest position we can cover
    # using fountains available up to the current scan position.
    farthest_reach = 0

    # Start scanning garden positions from 1 to n.
    for position in range(1, n + 1):

        # Update the farthest reach using fountains whose coverage starts here.
        farthest_reach = max(farthest_reach, max_reach_from_start[position])

        # If this position is not covered yet, we must activate one more fountain.
        if position > current_end:

            # If farthest_reach is still before current position,
            # then this position cannot be covered.
            # In this problem, usually this case will not happen,
            # but we keep it for safety.
            if farthest_reach < position:
                return -1

            # Activate one fountain.
            fountains_count += 1

            # After activating the best available fountain,
            # all positions up to farthest_reach are now covered.
            current_end = farthest_reach

    # Return minimum number of fountains required.
    return fountains_count

from typing import List


def fountainActivation(locations: List[int]) -> int:
    # Store total number of garden positions.
    n = len(locations)

    # If there are no positions, no fountain is needed.
    if n == 0:
        return 0

    # max_reach_from_start[left] stores the farthest right position
    # covered by any fountain starting at left.
    max_reach_from_start = [0] * (n + 1)

    # Convert every fountain into an interval.
    for index, radius in enumerate(locations):

        # Convert 0-based index to 1-based position.
        position = index + 1

        # Find left boundary safely.
        left = max(1, position - radius)

        # Find right boundary safely.
        right = min(n, position + radius)

        # Keep the farthest right coverage for this left point.
        max_reach_from_start[left] = max(max_reach_from_start[left], right)

    # Count selected fountains.
    fountains_count = 0

    # End position currently covered.
    current_end = 0

    # Best farthest reach available so far.
    farthest_reach = 0

    # Scan every garden position.
    for position in range(1, n + 1):

        # Include fountain coverage starting from this position.
        farthest_reach = max(farthest_reach, max_reach_from_start[position])

        # If current position is outside already covered range,
        # we need to select another fountain.
        if position > current_end:

            # Safety check for impossible coverage.
            if farthest_reach < position:
                return -1

            # Select one more fountain.
            fountains_count += 1

            # Extend covered range.
            current_end = farthest_reach

    # Return final minimum count.
    return fountains_count


def run_test(test_name: str, locations: List[int], expected: int) -> None:
    # Call the main solution function.
    actual = fountainActivation(locations)

    # Compare actual output with expected output.
    result = "PASS" if actual == expected else "FAIL"

    # Print test result clearly.
    print(f"{test_name}: {result} | Expected = {expected}, Actual = {actual}")


def main() -> None:
    # Sample Case 0:
    # Position 2 covers full garden from 1 to 3.
    run_test("Sample Case 0", [1, 1, 1], 1)

    # Example from problem:
    # Fountain at position 2 covers 1 to 3.
    run_test("Example Case", [1, 2, 1], 1)

    # Sample Case 1:
    # Fountain at position 1 covers 1 to 3,
    # and fountain at position 4 covers position 4.
    run_test("Sample Case 1", [2, 0, 0, 0], 2)

    # All fountains cover only themselves.
    # Need all fountains.
    run_test("No Extra Coverage", [0, 0, 0, 0], 4)

    # One big fountain in the middle covers everything.
    run_test("Middle Fountain Covers All", [0, 0, 5, 0, 0], 1)

    # Large data case:
    # First fountain covers all positions.
    large_locations = [100000] + [0] * 99999
    run_test("Large Data Case", large_locations, 1)

    # Another large data case:
    # Every fountain covers only itself.
    # Need all 100000 fountains.
    large_zero_locations = [0] * 100000
    run_test("Large Zero Coverage Case", large_zero_locations, 100000)


if __name__ == "__main__":
    main()