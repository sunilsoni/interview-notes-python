def solution(matrix):
    """
    Finds the length of the longest diagonal segment that matches the pattern:
    1, 2, 0, 2, 0, 2, 0, ...
    and that finishes because the next diagonal step would be out-of-bounds
    (i.e. the segment naturally ends at a border).

    In a matrix larger than 1×1, we require that a valid segment contains at least 3 elements.
    (A 1×1 matrix is a special case where the only cell is valid.)

    Args:
        matrix (list of list of int): 2D matrix with values 0, 1, or 2.

    Returns:
        int: The length of the longest valid diagonal segment, or 0 if none exists.
    """
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix)
    m = len(matrix[0])

    # Define the four possible diagonal directions: (dx, dy)
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def in_bounds(i, j):
        return 0 <= i < n and 0 <= j < m

    # Given a position index in the segment, return the expected value.
    def expected_value(pos):
        if pos == 0:
            return 1
        # For positions >=1: odd positions should be 2 and even positions (other than 0) should be 0.
        return 2 if pos % 2 == 1 else 0

    max_length = 0

    # For every cell that might be the start of a segment (it must contain 1)
    for i in range(n):
        for j in range(m):
            if matrix[i][j] != 1:
                continue  # only start where the cell equals 1

            # Try each of the four diagonal directions
            for dx, dy in directions:
                cur_i, cur_j = i, j
                seg_length = 1  # already matched the starting cell

                while True:
                    next_i = cur_i + dx
                    next_j = cur_j + dy
                    if in_bounds(next_i, next_j):
                        # We can continue – check if the next cell matches the expected pattern.
                        exp = expected_value(seg_length)
                        if matrix[next_i][next_j] != exp:
                            # Mismatch encountered while still in bounds.
                            # In that case we do not consider this segment at all.
                            seg_length = 0
                            break
                        # Otherwise, the cell matches; update the current cell and extend the segment.
                        cur_i, cur_j = next_i, next_j
                        seg_length += 1
                    else:
                        # Next cell is out-of-bounds: the segment "naturally" finishes at the border.
                        # But accept it only if the last cell (cur_i, cur_j) is on a border.
                        # And if the matrix is larger than 1x1, require that seg_length >= 3.
                        if (cur_i == 0 or cur_i == n - 1 or cur_j == 0 or cur_j == m - 1):
                            if (n == 1 and m == 1) or seg_length >= 3:
                                max_length = max(max_length, seg_length)
                        break

    return max_length


# -----------------------------------------------------------------------------
# The following is a simple main method for testing the solution with several cases.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    tests = [
        {
            "description": "Test case 1",
            "matrix": [
                [2, 1, 2, 2, 0],
                [0, 2, 0, 2, 2],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 2, 2],
                [2, 2, 0, 2, 0]
            ],
            "expected": 3
        },
        {
            "description": "Test case 2 (1x1 matrix)",
            "matrix": [[1]],
            "expected": 1
        },
        {
            "description": "Test case 3 (no valid segment)",
            "matrix": [
                [0, 2, 1],
                [1, 0, 2],
                [2, 1, 0]
            ],
            "expected": 0
        },
        {
            "description": "Test case 4 (no valid segment: segment stops before border)",
            "matrix": [
                [1, 0, 0, 0],
                [0, 2, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],
            "expected": 0
        },
        {
            "description": "Test case 5 (valid long segment)",
            "matrix": [
                [1, 0, 0, 0, 0],
                [0, 2, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0]
            ],
            "expected": 5
        }
    ]

    all_passed = True
    for test in tests:
        result = solution(test["matrix"])
        if result == test["expected"]:
            print(f"{test['description']} PASS: Output = {result}, Expected = {test['expected']}")
        else:
            print(f"{test['description']} FAIL: Output = {result}, Expected = {test['expected']}")
            all_passed = False

    # Large Input Test:
    # Create a 100x100 matrix and embed a valid diagonal segment along the down-right direction.
    n, m = 100, 100
    large_matrix = [[0 for _ in range(m)] for _ in range(n)]
    # Choose a starting point near the bottom-right border so that the diagonal touches the border.
    start_i, start_j = 90, 90
    max_steps = min(n - start_i, m - start_j)  # maximum steps until out-of-bounds
    for step in range(max_steps):
        if step == 0:
            large_matrix[start_i + step][start_j + step] = 1
        else:
            # Expected pattern: index 1 → 2, index 2 → 0, index 3 → 2, index 4 → 0, etc.
            large_matrix[start_i + step][start_j + step] = 2 if step % 2 == 1 else 0

    # The valid segment should have length equal to max_steps if max_steps>=3.
    expected_large = max_steps if max_steps >= 3 else 0
    large_result = solution(large_matrix)
    if large_result == expected_large:
        print(f"Large Input Test PASS: Output = {large_result}, Expected = {expected_large}")
    else:
        print(f"Large Input Test FAIL: Output = {large_result}, Expected = {expected_large}")
        all_passed = False

    if all_passed:
        print("All test cases passed!")
    else:
        print("Some test cases failed.")
