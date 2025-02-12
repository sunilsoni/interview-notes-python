def check_pattern(matrix, start_i, start_j, di, dj, rows, cols):
    """
    Check diagonal pattern starting from given position and direction
    Returns length of valid pattern if pattern ends at border, 0 otherwise
    """
    if matrix[start_i][start_j] != 1:  # Must start with 1
        return 0

    length = 1
    i, j = start_i + di, start_j + dj
    expect_two = True  # After 1, expect 2

    while 0 <= i < rows and 0 <= j < cols:
        current = matrix[i][j]
        if expect_two:
            if current != 2:
                break
            expect_two = False
        else:
            if current != 0:
                break
            expect_two = True

        length += 1
        i += di
        j += dj

    # Check if we reached a border
    if i < 0 or i >= rows or j < 0 or j >= cols:
        return length
    return 0


def solution(matrix):
    if not matrix or not matrix[0]:
        return 0

    rows = len(matrix)
    cols = len(matrix[0])
    max_length = 0

    # Diagonal directions: up-right, up-left, down-right, down-left
    directions = [(-1, 1), (-1, -1), (1, 1), (1, -1)]

    # Check from each starting position
    for i in range(rows):
        for j in range(cols):
            for di, dj in directions:
                length = check_pattern(matrix, i, j, di, dj, rows, cols)
                max_length = max(max_length, length)

    return max_length


def test_solution():
    test_cases = [
        {
            "input": [
                [2, 1, 2, 2, 0],
                [0, 2, 0, 2, 2],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 2, 2],
                [2, 2, 0, 2, 0]
            ],
            "expected": 3,
            "description": "Example case"
        },
        {
            "input": [[1, 2, 0]],
            "expected": 3,
            "description": "Single row"
        },
        {
            "input": [[1], [2], [0]],
            "expected": 3,
            "description": "Single column"
        },
        {
            "input": [[0]],
            "expected": 0,
            "description": "Single element"
        },
        {
            "input": [
                [1, 2, 0, 2, 0],
                [0, 1, 2, 0, 2],
                [0, 0, 1, 2, 0]
            ],
            "expected": 5,
            "description": "Perfect diagonal pattern"
        }
    ]

    passed = 0
    total = len(test_cases)

    for i, test_case in enumerate(test_cases, 1):
        result = solution(test_case["input"])
        status = "PASS" if result == test_case["expected"] else "FAIL"

        print(f"\nTest #{i}: {test_case['description']}")
        print(f"Expected: {test_case['expected']}")
        print(f"Got: {result}")
        print(f"Status: {status}")

        if status == "PASS":
            passed += 1

    print(f"\nSummary: {passed}/{total} tests passed")


if __name__ == "__main__":
    test_solution()
