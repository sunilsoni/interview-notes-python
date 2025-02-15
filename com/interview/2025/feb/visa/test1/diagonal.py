def solution(matrix):
    """
    Finds the longest diagonal segment matching the repeating pattern:
      1, 2, 0, 2, 0, 2, 0, ...
    The segment must end on the matrix border.
    """
    n = len(matrix)
    m = len(matrix[0]) if n else 0

    if n == 0 or m == 0:
        return 0

    def pattern_value(index):
        """Value at position 'index' in the sequence 1,2,0,2,0,2,0,..."""
        # index=0 -> 1
        # index=1 -> 2
        # index=2 -> 0
        # index=3 -> 2
        # index=4 -> 0, ...
        return 1 if index == 0 else (2 if (index % 2 == 1) else 0)

    def on_border(r, c):
        """Check if (r,c) is on the outer border of the matrix."""
        return (r == 0 or r == n - 1 or c == 0 or c == m - 1)

    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    max_length = 0

    for r in range(n):
        for c in range(m):
            # Only start if we have a '1' at this cell
            if matrix[r][c] == 1:
                for (dr, dc) in directions:
                    rr, cc = r, c
                    pattern_index = 0

                    # Move along the diagonal while cells match the pattern
                    while 0 <= rr < n and 0 <= cc < m \
                            and matrix[rr][cc] == pattern_value(pattern_index):
                        pattern_index += 1
                        rr += dr
                        cc += dc

                    # Last valid cell is one step back
                    last_r = rr - dr
                    last_c = cc - dc
                    current_length = pattern_index

                    # Check if that last valid cell is on the border
                    if 0 <= last_r < n and 0 <= last_c < m:
                        if on_border(last_r, last_c):
                            max_length = max(max_length, current_length)

    return max_length


def main():
    test_cases = [
        # Test 1 (problem statement example)
        (
            [
                [2, 1, 2, 2, 0],
                [0, 2, 0, 2, 2],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 2, 2],
                [2, 2, 0, 2, 0]
            ],
            3
        ),
        # Test 2: single element '1' => length 1
        (
            [[1]],
            1
        ),
        # Test 3: no '1' => 0
        (
            [
                [2, 0],
                [0, 2]
            ],
            0
        ),
        # Test 4: small diagonal with 1->2->0 => length 3
        (
            [
                [1, 0, 0],
                [0, 2, 0],
                [0, 0, 0]
            ],
            3
        ),
        # Test 5: all 2/0, no '1' => 0
        (
            [
                [2, 2, 2],
                [2, 0, 2],
                [2, 2, 2]
            ],
            0
        ),
        # Test 6: user expects 3, code finds 2
        (
            [
                [0, 1, 0, 2],
                [2, 0, 2, 0],
                [1, 2, 0, 2],
                [2, 0, 2, 0]
            ],
            3
        ),
    ]

    print("Running Tests:")
    for i, (matrix_data, expected) in enumerate(test_cases, start=1):
        got = solution(matrix_data)
        if got == expected:
            print(f"Test {i} PASS | Expected: {expected}, Got: {got}")
        else:
            print(f"Test {i} FAIL | Expected: {expected}, Got: {got}")


if __name__ == "__main__":
    main()
