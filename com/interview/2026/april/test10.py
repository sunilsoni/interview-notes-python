def optimal_path_dfs(grid):
    # Safety check: if the grid is completely empty, we can't collect anything
    if not grid or not grid[0]:
        return 0

    # Get the total number of rows and columns from the grid boundaries
    rows = len(grid)
    cols = len(grid[0])

    # Create a memory bank (dictionary) to store results we've already calculated
    # The key will be (row, col) and the value will be the max rocks from that point to the end
    memo = {}

    def get_neighbors(r, c):
        """
        Helper function to find where we can move next.
        Since the problem says we can only move North (up) or East (right):
        - North means row decreases: (r - 1, c)
        - East means column increases: (r, c + 1)
        """
        neighbors = []

        # Check if moving North (up) stays inside the top boundary of the grid
        if r - 1 >= 0:
            # If valid, add the coordinates of the northern neighbor to our list
            neighbors.append((r - 1, c))

        # Check if moving East (right) stays inside the right boundary of the grid
        if c + 1 < cols:
            # If valid, add the coordinates of the eastern neighbor to our list
            neighbors.append((r, c + 1))

        # Return the list of valid next steps (will have 0, 1, or 2 neighbors)
        return neighbors

    def dfs(r, c):
        """
        Core DFS function that explores paths recursively.
        It calculates: 'Max rocks collectible from (r, c) to the destination'
        """
        # Base Case: Check if we have reached the destination (Top-Right corner)
        if r == 0 and c == cols - 1:
            # If we are at the finish line, the score is just the rocks sitting in this cell
            return grid[r][c]

        # DP Check: Have we already calculated the best path from this exact cell before?
        if (r, c) in memo:
            # If yes, return the saved answer instantly instead of re-calculating
            return memo[(r, c)]

        # Initialize a variable to keep track of the best score found from our neighbors
        max_from_next_steps = 0

        # Look at all valid neighboring cities we can step into from here
        for next_r, next_c in get_neighbors(r, c):
            # Recursively ask DFS for the maximum score possible from that neighbor
            neighbor_score = dfs(next_r, next_c)
            # Update our tracker if this neighbor gives us a higher rock total
            max_from_next_steps = max(max_from_next_steps, neighbor_score)

        # The total max rocks from THIS cell is its own rocks PLUS the best score ahead
        memo[(r, c)] = grid[r][c] + max_from_next_steps

        # Return the final calculated value for this cell
        return memo[(r, c)]

    # Kick off the process by starting our DFS at the bottom-left corner
    # Row index for bottom is (rows - 1), column index for left is 0
    return dfs(rows - 1, 0)