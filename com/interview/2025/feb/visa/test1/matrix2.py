def solution(matrix):
    """
    Finds the length of the longest diagonal segment that matches the pattern:
      1, 0, 2, 0, 2, 0, …
    and that ends at a matrix border.

    A segment:
      - May start at any matrix element that is 1.
      - May proceed in any one of the four diagonal directions.
      - Is only valid if its final cell lies on the border of the matrix.
    """
    n = len(matrix)
    m = len(matrix[0])

    # Four diagonal directions: down-right, down-left, up-right, up-left.
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def is_border(r, c):
        """Return True if (r, c) is on a border of the matrix."""
        return r == 0 or r == n - 1 or c == 0 or c == m - 1

    def expected_value(idx):
        """
        Returns the expected number at position idx in the segment.
        With the pattern interpreted as: 1, 0, 2, 0, 2, 0, ...
          - idx 0 -> 1
          - For idx >= 1: odd positions should be 0 and even positions (>=2) should be 2.
        """
        if idx == 0:
            return 1
        return 0 if idx % 2 == 1 else 2

    max_length = 0

    # Try every cell as a potential starting point.
    for i in range(n):
        for j in range(m):
            if matrix[i][j] != 1:
                continue  # The segment must start with 1.
            # For each starting point, check all four diagonal directions.
            for dr, dc in directions:
                length = 0  # Number of cells in this segment so far.
                r, c = i, j
                idx = 0  # Position in the expected pattern.
                valid_length = 0  # Length recorded when a border is reached.
                while 0 <= r < n and 0 <= c < m:
                    if matrix[r][c] != expected_value(idx):
                        break  # Pattern mismatch: stop extending this segment.
                    length += 1
                    # If current cell is on border, record current segment length.
                    if is_border(r, c):
                        valid_length = length
                    r += dr
                    c += dc
                    idx += 1
                max_length = max(max_length, valid_length)

    return max_length


# A simple main method for testing
if __name__ == '__main__':
    def run_test(test_id, matrix, expected):
        result = solution(matrix)
        if result == expected:
            print(f"Test {test_id}: PASS")
        else:
            print(f"Test {test_id}: FAIL (Expected {expected}, got {result})")


    # Test 1: Provided test case.
    matrix1 = [
        [2, 1, 2, 2, 0],
        [0, 2, 0, 2, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 2, 2],
        [2, 2, 0, 2, 0]
    ]
    # With the pattern 1,0,2,0,2,... the longest segment is:
    # starting from (3,2)=1, then (2,3)=0, then (1,4)=2.
    run_test(1, matrix1, 3)

    # Test 2: Single-cell matrix (already on border).
    matrix2 = [[1]]
    run_test(2, matrix2, 1)

    # Test 3: Matrix with no starting 1.
    matrix3 = [
        [0, 2],
        [2, 0]
    ]
    run_test(3, matrix3, 0)

    # Test 4: Valid diagonal segment longer than 1.
    # Starting at (0,0)=1, then (1,1)=? expected: index1 should be 0.
    # Let's construct a diagonal: 1, 0, 2, 0.
    matrix4 = [
        [1, 9, 9, 9],
        [9, 0, 9, 9],
        [9, 9, 2, 9],
        [9, 9, 9, 0]
    ]
    # The segment from (0,0)->(1,1)->(2,2)->(3,3) is 1,0,2,0 and (3,3) is border.
    run_test(4, matrix4, 4)

    # Test 5: Segment that stops before reaching a border (thus not valid).
    matrix5 = [
        [9, 9, 9, 9, 9],
        [9, 1, 0, 2, 9],
        [9, 9, 9, 9, 9],
        [9, 9, 9, 9, 9],
        [9, 9, 9, 9, 9]
    ]
    # Starting from (1,1)=1, direction (1,1): (1,1)=1, (2,2)=9 (mismatch) -> segment stops.
    # Only possible valid segment would be of length 1 if (1,1) were on a border, but it isn’t.
    run_test(5, matrix5, 0)

    # Test 6: Stress test with a larger matrix.
    size = 50
    # Initialize with dummy values (e.g. 9) so that only the intended diagonal has our pattern.
    matrix6 = [[9] * size for _ in range(size)]
    # Construct a diagonal segment from the top-left corner (which is on the border) downward.
    # Pattern: 1, 0, 2, 0, 2, 0, ...
    for k in range(size):
        if k == 0:
            matrix6[k][k] = 1
        else:
            matrix6[k][k] = 0 if k % 2 == 1 else 2
    run_test(6, matrix6, size)
