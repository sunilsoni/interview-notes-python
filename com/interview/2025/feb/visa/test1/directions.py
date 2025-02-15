def solution(matrix):
    """
    Finds the length of the longest diagonal segment that matches the pattern:
    1, 2, 0, 2, 0, 2, ... and finishes at a matrix border.

    Args:
    matrix (list of list of int): 2D matrix with values 0, 1, or 2.

    Returns:
    int: The length of the longest valid diagonal segment.
    """
    if not matrix or not matrix[0]:
        return 0

    n = len(matrix)
    m = len(matrix[0])

    # Define the four diagonal directions: (dx, dy)
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def in_bounds(i, j):
        return 0 <= i < n and 0 <= j < m

    def is_border(i, j):
        # Returns True if (i,j) is on the border (first/last row or first/last column)
        return i == 0 or i == n - 1 or j == 0 or j == m - 1

    def expected_value(pos):
        # pos: the index in the segment (0-indexed)
        if pos == 0:
            return 1
        # For pos >= 1, odd positions must be 2, even positions must be 0.
        return 2 if pos % 2 == 1 else 0

    max_length = 0

    # Iterate over all cells
    for i in range(n):
        for j in range(m):
            # Only start if the cell's value is 1 (pattern must start with 1)
            if matrix[i][j] != 1:
                continue

            # For each of the four diagonal directions
            for dx, dy in directions:
                # Start simulation from (i, j)
                curr_i, curr_j = i, j
                seg_length = 1  # we have matched the first element (1)

                # We continue extending the segment until we break due to out-of-bound or mismatch.
                while True:
                    next_i = curr_i + dx
                    next_j = curr_j + dy
                    # If next cell is out-of-bound, then the segment ends here.
                    if not in_bounds(next_i, next_j):
                        # Valid segment only if the last cell is on border.
                        if is_border(curr_i, curr_j):
                            max_length = max(max_length, seg_length)
                        break

                    # Determine the expected value at the next position in the segment.
                    exp_val = expected_value(seg_length)
                    if matrix[next_i][next_j] != exp_val:
                        # If pattern mismatches, segment ends.
                        # Only record it if the last valid cell is on border.
                        if is_border(curr_i, curr_j):
                            max_length = max(max_length, seg_length)
                        break

                    # Pattern matched: update current position and segment length.
                    curr_i, curr_j = next_i, next_j
                    seg_length += 1

                    # If the new current cell is on border and the next step is out-of-bound,
                    # then in the next iteration we'll exit. But we can also record here if desired.
                    # However, we record only when the segment terminates.

    return max_length


# A simple main method for testing the solution
if __name__ == "__main__":
    tests = [
        {
            "matrix": [
                [2, 1, 2, 2, 0],
                [0, 2, 0, 2, 2],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 2, 2],
                [2, 2, 0, 2, 0]
            ],
            "expected": 3
        },
        # Additional test cases:
        # 1x1 matrix: only valid if cell==1 and is on border (which it is)
        {
            "matrix": [[1]],
            "expected": 1
        },
        # A matrix where no diagonal segment fully matches the pattern (return 0)
        {
            "matrix": [
                [0, 2, 1],
                [1, 0, 2],
                [2, 1, 0]
            ],
            "expected": 0
        },
        # A case where a diagonal segment is longer:
        {
            "matrix": [
                [1, 2, 0, 2],
                [0, 1, 2, 0],
                [2, 0, 1, 2],
                [2, 2, 0, 1]
            ],
            # One valid segment: start at (1,0)=0? no.
            # But consider starting at (2,0) if it were 1... Let's adjust below.
            # We'll design a matrix with a known diagonal: start at (0,0)=1, then (1,1)=2, (2,2)=0, (3,3)=2.
            # However, note that pattern after 1 should be 2, then 0, then 2, then 0,... So (3,3) should be 0.
            # Let's use a different matrix:
            "matrix": [
                [1, 0, 0, 0],
                [0, 2, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ],
            # Here starting at (0,0)=1, then (1,1)=2, then (2,2)=0; (3,3) would be expected to be 2 but is 0.
            # So the longest valid segment is of length 3, and (2,2) is border? Actually (2,2) is not on border in a 4x4 matrix.
            # So no valid segment here.
            "expected": 0
        },
        # A designed test where a valid long segment exists:
        {
            "matrix": [
                [1, 0, 0, 0, 0],
                [0, 2, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0]
            ],
            # Consider starting at (0,0)=1, then (1,1)=2, then (2,2)=0, then (3,3)=? expected 2, but matrix[3][3]==2,
            # then (4,4)=? expected 0, matrix[4][4]==0, and (4,4) is on border (last row and col).
            # This yields a segment of length 5.
            "expected": 5
        }
    ]

    all_passed = True
    for idx, test in enumerate(tests):
        result = solution(test["matrix"])
        if result == test["expected"]:
            print(f"Test case {idx + 1} PASS: Output = {result}, Expected = {test['expected']}")
        else:
            print(f"Test case {idx + 1} FAIL: Output = {result}, Expected = {test['expected']}")
            all_passed = False

    # Testing with a large data input.
    # Let's create a 100x100 matrix filled with 0's and then place a valid long diagonal.
    # For example, we can embed a diagonal starting at (10,10) that follows the pattern until the border.
    n, m = 100, 100
    large_matrix = [[0] * m for _ in range(n)]

    # Choose a starting point and a diagonal direction, e.g., down-right.
    start_i, start_j = 10, 10
    # Determine the maximum possible steps until a border in down-right direction.
    max_steps = min(n - start_i, m - start_j)
    # Fill the diagonal according to the pattern: pattern[0]=1, pattern[1]=2, pattern[2]=0, pattern[3]=2, ...
    for step in range(max_steps):
        if step == 0:
            large_matrix[start_i + step][start_j + step] = 1
        else:
            large_matrix[start_i + step][start_j + step] = 2 if step % 2 == 1 else 0

    # The expected length is max_steps provided the last cell (start_i + max_steps - 1, start_j + max_steps - 1) is on border.
    # Our large matrix has indices 0...99, so to ensure the diagonal ends at a border, we can adjust start.
    # Let's choose start_i = start_j = 90 so that max_steps = min(100-90, 100-90) = 10, and (99,99) is on border.
    start_i, start_j = 90, 90
    max_steps = min(n - start_i, m - start_j)
    for step in range(max_steps):
        if step == 0:
            large_matrix[start_i + step][start_j + step] = 1
        else:
            large_matrix[start_i + step][start_j + step] = 2 if step % 2 == 1 else 0

    expected_large = max_steps  # since the diagonal from (90,90) to (99,99) matches the pattern
    large_result = solution(large_matrix)
    if large_result >= expected_large:
        # It might find another segment that is as long or longer.
        print(f"Large Input Test PASS: Output = {large_result}, Expected at least = {expected_large}")
    else:
        print(f"Large Input Test FAIL: Output = {large_result}, Expected at least = {expected_large}")
        all_passed = False

    if all_passed:
        print("All test cases passed!")
    else:
        print("Some test cases failed.")
