def find_largest_shape(grid):
    # Convert input string grid to 2D list for easier processing
    grid = [list(row) for row in grid.strip().split('\n')]
    rows, cols = len(grid), len(grid[0])

    def explore_shape(r, c):
        # Base cases: out of bounds or not a black pixel
        if (r < 0 or r >= rows or
                c < 0 or c >= cols or
                grid[r][c] != 'X'):
            return 0

        # Mark this pixel as visited by changing it to '.'
        grid[r][c] = '.'

        # Recursively explore all 4 directions and sum the areas
        size = 1  # Count current pixel
        # Check up, down, left, right
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            size += explore_shape(r + dr, c + dc)
        return size

    max_size = 0
    # Iterate through each cell in the grid
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 'X':
                # Found a black pixel, explore its shape
                shape_size = explore_shape(i, j)
                max_size = max(max_size, shape_size)

    return max_size


def test_cases():
    # Test Case 1: Example from question
    test1 = """
.......
.XXX...
.XX..X.
.XXX.XXX
.......
""".strip()
    assert find_largest_shape(test1) == 8, "Test 1 Failed"

    # Test Case 2: Second example
    test2 = """
.......
.XXX...
.XX....
.XX....
.......
""".strip()
    assert find_largest_shape(test2) == 6, "Test 2 Failed"

    # Test Case 3: Empty grid
    test3 = """
.....
.....
.....
""".strip()
    assert find_largest_shape(test3) == 0, "Test 3 Failed"

    # Test Case 4: Single pixel
    test4 = """
....
.X..
....
""".strip()
    assert find_largest_shape(test4) == 1, "Test 4 Failed"

    # Test Case 5: Large grid (20x20)
    large_grid = ('.' * 20 + '\n') * 9 + ('X' * 20 + '\n') + ('.' * 20 + '\n') * 10
    assert find_largest_shape(large_grid.strip()) == 20, "Test 5 Failed"

    print("All test cases passed!")


if __name__ == "__main__":
    test_cases()
