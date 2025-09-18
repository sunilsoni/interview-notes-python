def min_rooks_left(board):
    """
    Returns the minimal number of Rooks left after all possible captures,
    using maximum bipartite matching between rows and columns.
    """

    # Edge case: empty board or no Rooks at all
    if not board or not board[0]:
        return 0

    m, n = len(board), len(board[0])  # Number of rows (m) and columns (n)

    # Step 1: Build bipartite graph as adjacency list
    from collections import defaultdict

    graph = defaultdict(list)  # key: row, value: list of columns with a Rook
    for i in range(m):
        for j in range(n):
            if board[i][j] == 1:
                graph[i].append(j)  # Connect row i to column j

    # Step 2: Hungarian Algorithm / DFS-based matching
    def bpm(row, visited, match):
        """
        Try to find an augmenting path for row 'row'.
        """
        for col in graph[row]:
            if not visited[col]:
                visited[col] = True  # Mark this column as visited in this path
                # If col is not matched or can be rematched, match it to this row
                if match[col] == -1 or bpm(match[col], visited, match):
                    match[col] = row  # Assign row to this column
                    return True
        return False

    match = [-1] * n  # match[col] = row matched to this column (else -1)
    result = 0        # Count of matchings found

    # Try to find a match for every row with a Rook
    for row in graph:
        visited = [False] * n  # Reset visited columns for this DFS
        if bpm(row, visited, match):
            result += 1

    # Each matching corresponds to one Rook left on the board (cannot capture anymore)
    return result

# ---------------------- MAIN TEST METHOD ------------------------

def run_tests():
    # Define test cases as (input, expected output)
    test_cases = [
        (
            [
                [0, 0, 1, 0],
                [1, 0, 1, 0],
                [0, 0, 0, 1]
            ],
            2
        ),
        (
            [
                [1, 0, 0, 1],
                [0, 0, 0, 0],
                [1, 0, 0, 1]
            ],
            1
        ),
        (
            [
                [1, 1],
                [1, 1]
            ],
            2  # two matchings: (row0-col0, row1-col1)
        ),
        (
            [
                [0, 0],
                [0, 0]
            ],
            0  # no rooks
        ),
        (
            [
                [1],
                [1],
                [1]
            ],
            1  # all in one column
        ),
        (
            [
                [1, 0, 1],
                [0, 1, 0],
                [1, 0, 1]
            ],
            3
        ),
    ]

    # Large data test (stress test)
    big_board = [[1 if (i+j)%2==0 else 0 for j in range(200)] for i in range(200)]
    test_cases.append((big_board, 200))

    all_pass = True
    for idx, (board, expected) in enumerate(test_cases, 1):
        result = min_rooks_left(board)
        status = "PASS" if result == expected else f"FAIL (Expected {expected}, got {result})"
        print(f"Test {idx}: {status}")
        if status != "PASS":
            all_pass = False

    if all_pass:
        print("All test cases passed!")
    else:
        print("Some test cases failed.")

# ------------------ Run Main Tests ---------------
if __name__ == "__main__":
    run_tests()
