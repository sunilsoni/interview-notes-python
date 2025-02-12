def solution(matrix):
    # Dimensions of the matrix
    n = len(matrix)
    m = len(matrix[0])

    # Define the four diagonal directions: (row change, col change)
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def is_border(r, c):
        """Check if the cell (r, c) is on the border of the matrix."""
        return r == 0 or r == n - 1 or c == 0 or c == m - 1

    def expected_value(idx):
        """
        For a given position in the segment (idx starting at 0),
        return the expected number:
         - 0: expected 1 (starting cell)
         - idx odd: expected 2
         - idx even (and >0): expected 0
        """
        if idx == 0:
            return 1
        return 2 if idx % 2 == 1 else 0

    max_length = 0  # To record the longest valid segment

    # Iterate over each cell in the matrix
    for i in range(n):
        for j in range(m):
            # Only consider starting points that have the value 1
            if matrix[i][j] != 1:
                continue
            # Try each of the four diagonal directions
            for dr, dc in directions:
                length = 0
                r, c = i, j
                idx = 0  # Position in the pattern
                current_valid_length = 0  # Latest valid segment length that ended at border
                while 0 <= r < n and 0 <= c < m:
                    if matrix[r][c] != expected_value(idx):
                        break  # Pattern no longer matches
                    length += 1
                    # If the current cell is on the border, record this as a valid segment.
                    if is_border(r, c):
                        current_valid_length = length
                    # Move to the next cell in the chosen diagonal direction
                    r += dr
                    c += dc
                    idx += 1
                # Update max_length if we found a longer valid segment in this direction
                max_length = max(max_length, current_valid_length)

    return max_length


# Simple main method for testing the solution
if __name__ == '__main__':
    def run_test(test_id, matrix, expected):
        result = solution(matrix)
        if result == expected:
            print(f"Test {test_id}: PASS")
        else:
            print(f"Test {test_id}: FAIL (Expected {expected}, got {result})")


    # Provided test case
    matrix1 = [
        [2, 1, 2, 2, 0],
        [0, 2, 0, 2, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 2, 2],
        [2, 2, 0, 2, 0]
    ]
    run_test(1, matrix1, 3)

    # Additional tests

    # Test 2: Minimal matrix with one element, which is on the border and equals 1.
    matrix2 = [[1]]
    run_test(2, matrix2, 1)

    # Test 3: A matrix where no 1 exists.
    matrix3 = [
        [0, 2],
        [2, 0]
    ]
    run_test(3, matrix3, 0)

    # Test 4: A matrix where a valid diagonal segment is longer.
    # Starting at (0,0)=1, then (1,1)=2, (2,2)=0, (3,3)=2 and (3,3) is border.
    matrix4 = [
        [1, 0, 0, 0],
        [0, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 2]
    ]
    run_test(4, matrix4, 4)

    # Test 5: A case where the segment does not finish on a border until later.
    matrix5 = [
        [0, 0, 0, 0, 0],
        [0, 1, 2, 0, 2],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    # Here, starting at (1,1)=1, next (2,2)=? but (2,2) is 0 so pattern 2 not matched.
    run_test(5, matrix5, 0)

    # Test 6: Larger input (stress test) with a diagonal segment in one corner.
    size = 50
    matrix6 = [[0] * size for _ in range(size)]
    # Construct a diagonal segment from (0,0) to (size-1, size-1) following the pattern.
    # We fill the diagonal accordingly.
    for k in range(size):
        if k == 0:
            matrix6[k][k] = 1
        else:
            matrix6[k][k] = 2 if k % 2 == 1 else 0
    run_test(6, matrix6, size)
