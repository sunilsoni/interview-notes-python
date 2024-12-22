
"""
Question 1: You are given an m x n matrix board containing letters 'X' and 'O', capture regions that are surrounded:

- **Connect**: A cell is connected to adjacent cells horizontally or vertically.
- **Region**: To form a region, connect every 'O' cell.
- **Surround**: The region is surrounded with 'X' cells if you can connect the region with 'X' cells and none of the region cells are on the border.

A surrounded region is captured by replacing all 'O's with 'X's in the input matrix board.

**Input**:
`board = [["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]]`

**Output**:
`[["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "O", "X", "X"]]`

"""
def solve(board):
    if not board or not board[0]:
        return
    rows, cols = len(board), len(board[0])

    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != 'O':
            return
        board[r][c] = 'A'  # Mark as safe
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    # Mark all border-connected 'O's
    for i in range(rows):
        if board[i][0] == 'O':
            dfs(i, 0)
        if board[i][cols - 1] == 'O':
            dfs(i, cols - 1)
    for j in range(cols):
        if board[0][j] == 'O':
            dfs(0, j)
        if board[rows - 1][j] == 'O':
            dfs(rows - 1, j)

    # Flip captured O's to X, revert 'A' back to O
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 'O':
                board[i][j] = 'X'
            elif board[i][j] == 'A':
                board[i][j] = 'O'


def test_solution():
    def test_case(board, expected):
        # Create a deep copy for testing
        import copy
        b_copy = copy.deepcopy(board)
        solve(b_copy)
        return b_copy == expected

    # Provided test case
    board1 = [
        ["X", "X", "X", "X"],
        ["X", "O", "O", "X"],
        ["X", "X", "O", "X"],
        ["X", "O", "X", "X"]
    ]
    expected1 = [
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "X", "X", "X"],
        ["X", "O", "X", "X"]
    ]
    print("Test Case 1:", "PASS" if test_case(board1, expected1) else "FAIL")

    # Edge case: empty board
    board2 = []
    expected2 = []
    print("Test Case 2 (empty):", "PASS" if test_case(board2, expected2) else "FAIL")

    # Edge case: all X
    board3 = [
        ["X", "X"],
        ["X", "X"]
    ]
    expected3 = [
        ["X", "X"],
        ["X", "X"]
    ]
    print("Test Case 3 (all X):", "PASS" if test_case(board3, expected3) else "FAIL")

    # Edge case: all O
    board4 = [
        ["O", "O", "O"],
        ["O", "O", "O"],
        ["O", "O", "O"]
    ]
    # After solution, border Os remain O, internal Os turn X
    expected4 = [
        ["O", "O", "O"],
        ["O", "X", "O"],
        ["O", "O", "O"]
    ]
    print("Test Case 4 (all O):", "PASS" if test_case(board4, expected4) else "FAIL")

    # Large data test (just a brief check)
    large_board = [["O" for _ in range(50)] for _ in range(50)]
    # Just run and ensure no error/timeout (not verifying output here for brevity)
    # Ideally we’d set specific patterns and verify expected results, but here we focus on performance.
    try:
        import time
        start = time.time()
        solve(large_board)
        end = time.time()
        print("Test Case 5 (large): PASS (ran in {:.4f}s)".format(end - start))
    except:
        print("Test Case 5 (large): FAIL (error/timeout)")


if __name__ == "__main__":
    test_solution()
