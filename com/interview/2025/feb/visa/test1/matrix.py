def solution(matrix):
    """
    Finds the length of the longest diagonal segment in a matrix that matches the pattern:
       1, 2, 0, 2, 0, 2, 0, …
    and that “finishes at a matrix border.”

    A segment is built by starting at a cell containing 1 and then moving in one of the four
    diagonal directions. When the next move is out–of–bounds (i.e. reached a border) and we have
    already taken at least one step beyond the starting 1, we add 1 to the length.

    For matrices larger than 1×1 only segments of length >= 2 count.

    Args:
        matrix (list of list of int): 2D matrix with elements 0, 1, or 2.

    Returns:
        int: The length of the longest valid diagonal segment.
    """
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix)
    m = len(matrix[0])

    # For a 1x1 matrix, if the only element is 1, we return 1.
    if n == 1 and m == 1:
        return 1 if matrix[0][0] == 1 else 0

    # Define the four diagonal directions.
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def in_bounds(i, j):
        return 0 <= i < n and 0 <= j < m

    def is_border(i, j):
        # A cell is on the border if it is in the first or last row or column.
        return i == 0 or i == n - 1 or j == 0 or j == m - 1

    def expected_value(index):
        # index 0 must be 1; then odd indices: 2, even indices (>=2): 0.
        if index == 0:
            return 1
        return 2 if index % 2 == 1 else 0

    max_length = 0

    # For every cell that is a potential starting point (must contain 1)
    for i in range(n):
        for j in range(m):
            if matrix[i][j] != 1:
                continue
            # Try all four diagonal directions
            for dx, dy in directions:
                # We'll simulate a segment starting at (i,j)
                seg_length = 1  # starting cell (index 0, which is 1)
                curr_i, curr_j = i, j
                # Walk along the chosen direction
                while True:
                    next_i = curr_i + dx
                    next_j = curr_j + dy
                    if in_bounds(next_i, next_j):
                        # Next cell is in bounds; expected value for the next position:
                        exp = expected_value(seg_length)
                        if matrix[next_i][next_j] != exp:
                            # Mismatch: stop here.
                            break
                        # Match: move on.
                        curr_i, curr_j = next_i, next_j
                        seg_length += 1
                    else:
                        # Next move is out-of–bounds.
                        # If we have advanced at least one step beyond the starting cell,
                        # then add one extra count to “finish” the segment.
                        if seg_length > 1:
                            seg_length += 1
                        break
                # A valid segment must finish at a border.
                # (Note: in our simulation, if we stopped because the next cell was out-of–bounds,
                # we already added the extra count; otherwise we stopped due to mismatch.)
                if in_bounds(curr_i, curr_j) and not is_border(curr_i, curr_j):
                    # The segment did not finish at a border.
                    seg_length = 0
                # Also, if seg_length is only 1 (i.e. we never advanced), consider it invalid.
                if seg_length < 2:
                    seg_length = 0
                max_length = max(max_length, seg_length)
    return max_length


# Simple main method for testing
if __name__ == "__main__":
    tests = [
        {
            "name": "Test case 1",
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
            "name": "Test case 2 (1x1 matrix)",
            "matrix": [[1]],
            "expected": 1
        },
        {
            "name": "Test case 3 (no valid segment)",
            "matrix": [
                [0, 2, 1],
                [1, 0, 2],
                [2, 1, 0]
            ],
            "expected": 0
        },
        {
            "name": "Test case 4 (no valid segment)",
            "matrix": [
                [1, 2, 0, 2],
                [0, 1, 2, 0],
                [2, 0, 1, 2],
                [2, 2, 0, 1]
            ],
            "expected": 0
        },
        {
            "name": "Test case 5",
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
            print(f"{test['name']} PASS: Output = {result}, Expected = {test['expected']}")
        else:
            print(f"{test['name']} FAIL: Output = {result}, Expected = {test['expected']}")
            all_passed = False

    # Testing with a large input.
    # Create a 100x100 matrix filled with 0's and then insert a valid long diagonal.
    n, m = 100, 100
    large_matrix = [[0 for _ in range(m)] for _ in range(n)]
    # We choose a starting point and a direction (down–right) so that the segment finishes at the border.
    start_i, start_j = 90, 90  # then maximum steps = 10 (cells from 90 to 99)
    max_steps = min(n - start_i, m - start_j)
    for step in range(max_steps):
        if step == 0:
            large_matrix[start_i + step][start_j + step] = 1
        else:
            # Expected: odd steps are 2, even steps (>=2) are 0.
            large_matrix[start_i + step][start_j + step] = 2 if step % 2 == 1 else 0
    # With our rule, when the next step (step max_steps) would go out–of–bounds, we add one extra count.
    expected_large = max_steps + 1  # because segment length becomes (max_steps) plus 1 finishing count.
    large_result = solution(large_matrix)
    if large_result >= expected_large:
        print(f"Large Input Test PASS: Output = {large_result}, Expected at least = {expected_large}")
    else:
        print(f"Large Input Test FAIL: Output = {large_result}, Expected at least = {expected_large}")
        all_passed = False

    if all_passed:
        print("All test cases passed!")
    else:
        print("Some test cases failed.")