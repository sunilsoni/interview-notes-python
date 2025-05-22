def longestIncreasingPath(matrix):
    # Check if matrix is empty
    if not matrix or not matrix[0]:
        return 0

    # Get matrix dimensions
    rows = len(matrix)
    cols = len(matrix[0])

    # Initialize cache for memoization to store computed results
    cache = {}

    # Define possible movement directions (up, down, left, right)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def dfs(row, col, prev):
        # Base case: out of bounds or current value <= previous value
        if (row < 0 or row >= rows or
                col < 0 or col >= cols or
                matrix[row][col] <= prev):
            return 0

        # If result already in cache, return it
        if (row, col) in cache:
            return cache[(row, col)]

        # Current cell value
        current = matrix[row][col]
        max_length = 1

        # Explore all four directions
        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            # Get maximum path length from current position
            length = 1 + dfs(new_row, new_col, current)
            max_length = max(max_length, length)

        # Store result in cache before returning
        cache[(row, col)] = max_length
        return max_length

    # Find maximum path starting from each cell
    result = 0
    for i in range(rows):
        for j in range(cols):
            result = max(result, dfs(i, j, float('-inf')))

    return result


def test():
    # Test case 1
    matrix1 = [[9, 9, 4], [6, 6, 8], [2, 1, 1]]
    expected1 = 4
    result1 = longestIncreasingPath(matrix1)
    print(f"Test 1: {'PASS' if result1 == expected1 else 'FAIL'}")

    # Test case 2
    matrix2 = [[3, 4, 5], [3, 2, 6], [2, 2, 1]]
    expected2 = 4
    result2 = longestIncreasingPath(matrix2)
    print(f"Test 2: {'PASS' if result2 == expected2 else 'FAIL'}")

    # Test case 3 (single element)
    matrix3 = [[1]]
    expected3 = 1
    result3 = longestIncreasingPath(matrix3)
    print(f"Test 3: {'PASS' if result3 == expected3 else 'FAIL'}")

    # Test case 4 (empty matrix)
    matrix4 = []
    expected4 = 0
    result4 = longestIncreasingPath(matrix4)
    print(f"Test 4: {'PASS' if result4 == expected4 else 'FAIL'}")

    # Test case 5 (large matrix)
    matrix5 = [[i + j for j in range(100)] for i in range(100)]
    result5 = longestIncreasingPath(matrix5)
    print(f"Test 5 (Large matrix): Result = {result5}")


if __name__ == "__main__":
    test()
