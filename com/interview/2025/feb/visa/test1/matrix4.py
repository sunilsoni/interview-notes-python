def solution(matrix):
    if not matrix or not matrix[0]:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    max_length = 0
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != 1:
                continue

            for dx, dy in directions:
                current_i, current_j = i, j
                next_i = i + dx
                next_j = j + dy
                step = 1
                current_len = 1

                while 0 <= next_i < rows and 0 <= next_j < cols:
                    expected = 2 if (step - 1) % 2 == 0 else 0
                    if matrix[next_i][next_j] != expected:
                        break
                    current_len += 1
                    current_i = next_i
                    current_j = next_j
                    step += 1
                    next_i += dx
                    next_j += dy

                if (current_i == 0 or current_i == rows - 1 or
                        current_j == 0 or current_j == cols - 1):
                    if current_len > max_length:
                        max_length = current_len

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
