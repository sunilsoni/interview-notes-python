def optimal_path(grid):
    # Check if the grid is entirely empty (None or zero length) to prevent errors
    if not grid:
        # If there is no grid, we can't collect rocks, so we return 0
        return 0

    # Check if the first row is empty to ensure we actually have columns
    if not grid[0]:
        # If there are no columns, we can't collect rocks, so return 0
        return 0

    # Calculate the total number of rows in our grid by getting its length
    rows = len(grid)

    # Calculate the total number of columns by getting the length of the first row
    cols = len(grid[0])

    # Create a new tracker grid (DP table) filled with 0s, exactly the same size as our map
    # We need this to keep track of the maximum score possible at every single step
    dp = [[0] * cols for _ in range(rows)]

    # Set our starting point (bottom-left corner) to the rocks available at that exact city
    # row index is (rows - 1) because indices start at 0. column index is 0.
    dp[rows - 1][0] = grid[rows - 1][0]

    # Fill out the first column (the leftmost edge of the map)
    # We loop backward from the second-to-last row up to the top row
    for r in range(rows - 2, -1, -1):
        # Because we are on the left edge, we can ONLY travel North (up) from the cell below
        # So, current max = max from the cell below + rocks in the current cell
        dp[r][0] = dp[r + 1][0] + grid[r][0]

    # Fill out the bottom row (the bottom edge of the map)
    # We loop forward from the second column to the last column
    for c in range(1, cols):
        # Because we are on the bottom edge, we can ONLY travel East (right) from the cell left
        # So, current max = max from the cell to the left + rocks in the current cell
        dp[rows - 1][c] = dp[rows - 1][c - 1] + grid[rows - 1][c]

    # Now we fill in the rest of the grid, cell by cell
    # Start one row above the bottom, and move upwards to the top (row 0)
    for r in range(rows - 2, -1, -1):
        # For each row, start one column to the right of the edge, moving to the right
        for c in range(1, cols):
            # Look at the cell directly below the current one and get its max rock count
            rocks_if_coming_from_south = dp[r + 1][c]

            # Look at the cell directly to the left of the current one and get its max rock count
            rocks_if_coming_from_west = dp[r][c - 1]

            # Find which previous path gave us more rocks (the one from below, or the one from the left)
            best_previous_path = max(rocks_if_coming_from_south, rocks_if_coming_from_west)

            # The max rocks for THIS cell = the best previous path + the rocks sitting in THIS cell
            dp[r][c] = grid[r][c] + best_previous_path

    # By the time the loops finish, the top-right corner holds the absolute maximum path total
    # We return the value stored in the top-right cell (row 0, last column)
    return dp[0][cols - 1]


def do_tests_pass():
    # We store our test cases as a list of tuples: (Input_Grid, Expected_Output)
    test_cases = [
        # Test Case 1: The standard example provided in the problem description
        (
            [
                [0, 0, 0, 0, 5],
                [0, 1, 1, 1, 0],
                [2, 0, 0, 0, 0]
            ],
            10
        ),
        # Test Case 2: An extremely small 1x1 grid (Edge Case)
        (
            [[7]],
            7
        ),
        # Test Case 3: A completely empty grid (Edge Case)
        (
            [],
            0
        ),
        # Test Case 4: A grid where no rocks are available anywhere
        (
            [
                [0, 0, 0],
                [0, 0, 0]
            ],
            0
        ),
        # Test Case 5: A larger 5x5 dataset to test scaling
        # Optimal path: Start bottom-left (1) -> right(1) -> right(1) -> up(0) -> up(9) -> up(0) -> up(1) -> right(1) -> right(1) = 15
        (
            [
                [1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 9, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1]
            ],
            15
        )
    ]

    all_passed = True

    # Loop through every test case in our list
    for index, (test_input, expected_answer) in enumerate(test_cases):
        # Call our function with the current test grid
        actual_answer = optimal_path(test_input)

        # Check if our function's answer matches the expected answer
        if actual_answer == expected_answer:
            # If it matches, print a success message
            print(f"Test Case {index + 1}: PASS (Got {actual_answer})")
        else:
            # If it fails, print a failure message detailing what went wrong
            print(f"Test Case {index + 1}: FAIL (Expected {expected_answer}, but got {actual_answer})")
            # Mark that at least one test failed
            all_passed = False

    # Return the final true/false result for the entire test suite
    return all_passed


# Standard Python boilerplate to run the main method
if __name__ == "__main__":
    # Run the test function and check its return value
    if do_tests_pass():
        # If it returned True, all tests were successful
        print("\nAll tests pass! The code is ready.")
    else:
        # If it returned False, something is broken
        print("\nNot all tests pass. Please review the failures above.")