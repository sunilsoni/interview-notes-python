# Python 3 solution: Largest shape (connected 'X' components using 4-direction adjacency)
# HIGH PRIORITY: Every line is commented to explain what it does and why we need it.

from collections import deque  # import deque in case you prefer BFS; kept for optional use
import random                  # import random for generating test data for large/random tests
import time                    # import time to measure runtime for large data performance info
from typing import List        # import typing hints for readability and maintainability


def largest_shape_area(grid: List[str]) -> int:
    """
    Compute the area (number of cells) of the largest 4-directionally connected 'X' shape.
    Uses iterative DFS for reliability on large inputs.
    """
    # If grid is empty (no rows), the largest shape is 0 by definition
    if not grid:
        return 0

    # Number of rows (m) in the grid
    m = len(grid)
    # Number of columns (n) in the grid; assumes all rows have the same length
    n = len(grid[0]) if m > 0 else 0

    # If there are no columns, also no shapes
    if n == 0:
        return 0

    # Create a 2D boolean visited array initialized to False for all cells
    # visited[r][c] == True means we've already counted that cell in a shape exploration
    visited = [[False] * n for _ in range(m)]

    # Variable to track the largest area found so far
    max_area = 0

    # Predefine the 4 orthogonal movement directions: up, down, left, right
    # Each tuple is (dr, dc) representing row and column deltas
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Iterate through every cell in the m x n grid
    for r in range(m):
        # Loop over each column in the current row
        for c in range(n):
            # We only start a new flood fill if:
            # 1) the cell contains 'X' (a black pixel), AND
            # 2) it hasn't been visited before
            if grid[r][c] == 'X' and not visited[r][c]:
                # Start an iterative DFS using a stack to avoid recursion depth issues
                stack = [(r, c)]     # push the starting cell onto the stack
                visited[r][c] = True # mark the starting cell as visited
                area = 0             # reset area for this new connected component

                # Process the stack until there are no more connected cells to visit
                while stack:
                    # Pop one cell from the stack (LIFO order) for DFS
                    cr, cc = stack.pop()
                    # Count current cell as part of this shape
                    area += 1

                    # Explore all 4 orthogonal neighbors
                    for dr, dc in directions:
                        # Compute neighbor coordinates
                        nr, nc = cr + dr, cc + dc
                        # Check bounds and whether the neighbor is an unvisited 'X'
                        if 0 <= nr < m and 0 <= nc < n:
                            if grid[nr][nc] == 'X' and not visited[nr][nc]:
                                # Mark neighbor as visited immediately (prevents duplicate pushes)
                                visited[nr][nc] = True
                                # Push neighbor onto stack to continue DFS
                                stack.append((nr, nc))

                # After finishing this component, update the maximum area if needed
                if area > max_area:
                    max_area = area

    # Return the largest area found after scanning all cells
    return max_area


# ---------- Optional cross-check helper for small grids ----------
def largest_shape_area_bfs_check(grid: List[str]) -> int:
    """
    A BFS-based version used for cross-checking correctness on small/random tests.
    Not used for performance; purpose is to validate the main algorithm.
    """
    # Same initial empty checks as the main function
    if not grid:
        return 0
    m, n = len(grid), len(grid[0]) if len(grid) > 0 else 0
    if n == 0:
        return 0

    # Initialize visited matrix
    visited = [[False] * n for _ in range(m)]
    # Define orthogonal directions
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # Track maximum area
    max_area = 0

    # Scan all cells
    for r in range(m):
        for c in range(n):
            # Start BFS only on unvisited 'X'
            if grid[r][c] == 'X' and not visited[r][c]:
                # Use deque for efficient queue operations
                q = deque()
                # Enqueue starting cell and mark visited
                q.append((r, c))
                visited[r][c] = True
                # Area counter for this component
                area = 0

                # Standard BFS loop
                while q:
                    cr, cc = q.popleft()
                    area += 1
                    # Visit neighbors
                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < m and 0 <= nc < n:
                            if grid[nr][nc] == 'X' and not visited[nr][nc]:
                                visited[nr][nc] = True
                                q.append((nr, nc))

                # Track maximum
                if area > max_area:
                    max_area = area

    return max_area


# ---------- Helpers for tests and I/O formatting ----------
def parse_grid(multiline: str) -> List[str]:
    """
    Convert a multi-line string (with newline-separated rows) into a list of row strings.
    Trims empty lines around. Validates all rows have equal length.
    """
    # Split by lines and keep only non-empty lines after stripping whitespace
    rows = [line.rstrip('\n') for line in multiline.strip('\n').split('\n')]
    # Optional: validate rectangular shape
    # If not rectangular, raise a clear error (helps catch malformed test inputs)
    if rows:
        n = len(rows[0])
        for i, row in enumerate(rows):
            if len(row) != n:
                raise ValueError(f"Row {i} has length {len(row)} != {n}. Grid must be rectangular.")
    return rows


def run_single_test(name: str, grid_lines: List[str], expected: int) -> bool:
    """
    Run a single test:
    - Calls the main solver
    - Compares result with expected
    - Prints PASS/FAIL with details
    - Returns True on pass, False on fail
    """
    # Compute the result using the main function
    result = largest_shape_area(grid_lines)
    # Compare against expected
    ok = (result == expected)
    # Print formatted outcome
    print(f"[{name}] expected={expected}, got={result} -> {'PASS' if ok else 'FAIL'}")
    return ok


def generate_random_grid(rows: int, cols: int, p_black: float) -> List[str]:
    """
    Generate a random grid of given size.
    Each cell is 'X' with probability p_black, else '.'.
    Useful for stress/performance tests and random correctness checks.
    """
    # Build list of strings row by row
    g = []
    for _ in range(rows):
        # For each row, decide each cell independently
        row = ''.join('X' if random.random() < p_black else '.' for _ in range(cols))
        g.append(row)
    return g


def quick_random_correctness_pass(trials: int = 50, rows: int = 15, cols: int = 20, p_black: float = 0.3) -> bool:
    """
    Randomized small tests:
    - Generate a small random grid,
    - Compare main DFS answer vs. BFS cross-check,
    - Repeat for several trials,
    - Stop early on any mismatch.
    Returns True if all match, else False.
    """
    for t in range(1, trials + 1):
        # Create a random grid with moderate density of 'X'
        grid = generate_random_grid(rows, cols, p_black)
        # Compute expected via BFS checker
        expected = largest_shape_area_bfs_check(grid)
        # Compute actual via main solver
        actual = largest_shape_area(grid)
        # If mismatch, print details and return False
        if expected != actual:
            print(f"[RANDOM TEST {t}] MISMATCH -> expected {expected}, got {actual}")
            # Optional: print the grid to help debugging
            for line in grid:
                print(line)
            return False
    # If all trials matched, print a brief summary and return True
    print(f"[RANDOM TESTS] All {trials} randomized checks passed (DFS == BFS).")
    return True


def main():
    """
    Simple main method to:
    - Run provided examples,
    - Run extra edge tests,
    - Do random small tests (cross-check),
    - Run a large data test to show performance.
    """
    print("=== Largest Shape in Black-and-White Image: Test Runner (Python 3) ===")

    # ---------------- Provided Example 1 ----------------
    ex1_str = """
.......
.XXX...
.XX..X.
.XXX.XXX
.......
"""
    # Parse the multi-line string into a list of row strings
    ex1_grid = parse_grid(ex1_str)
    # Expected output from the prompt
    ex1_expected = 8
    # Run and print PASS/FAIL
    run_single_test("Example 1", ex1_grid, ex1_expected)

    # ---------------- Provided Example 2 ----------------
    ex2_str = """
.......
.XXX...
.XX....
.XX....
.......
"""
    ex2_grid = parse_grid(ex2_str)
    ex2_expected = 6
    run_single_test("Example 2", ex2_grid, ex2_expected)

    # ---------------- Extra Edge Cases ----------------

    # Case: Empty grid -> 0
    run_single_test("Edge: Empty", [], 0)

    # Case: Single cell '.' -> 0
    run_single_test("Edge: SingleDot", ["."], 0)

    # Case: Single cell 'X' -> 1
    run_single_test("Edge: SingleX", ["X"], 1)

    # Case: All dots in a small grid -> 0
    run_single_test("Edge: AllDots", ["....", "....", "...."], 0)

    # Case: All X in a small grid 3x4 -> area = 12
    run_single_test("Edge: AllX", ["XXXX", "XXXX", "XXXX"], 12)

    # Case: One long skinny row with multiple components
    # Grid: X..XX.X  -> largest component sizes: [1,2,1], max = 2
    run_single_test("Edge: SkinnyRow", ["X..XX.X"], 2)

    # Case: One long skinny column with two components
    # Grid: ['X', '.', 'X', 'X'] -> components [1,2], max = 2
    run_single_test("Edge: SkinnyCol", ["X", ".", "X", "X"], 2)

    # Case: Complex small shape
    complex_grid = parse_grid("""
X.XX
XX..
..XX
.XXX
""")
    # Let's compute expected via checker (reduces manual counting mistakes)
    complex_expected = largest_shape_area_bfs_check(complex_grid)
    run_single_test("Edge: ComplexSmall", complex_grid, complex_expected)

    # ---------------- Randomized small tests (cross-check) ----------------
    # Compare DFS (main) vs BFS checker on random small grids
    quick_random_correctness_pass(trials=40, rows=12, cols=16, p_black=0.35)

    # ---------------- Large data performance test ----------------
    # Generate a large random grid (tune sizes as needed)
    rows, cols, p = 1200, 1200, 0.4  # ~1.44M cells, 40% black
    print(f"\n[Large Test] Generating {rows}x{cols} grid with p_black={p} ...")
    start_gen = time.time()
    big_grid = generate_random_grid(rows, cols, p)
    end_gen = time.time()
    print(f"[Large Test] Generation time: {end_gen - start_gen:.2f}s")

    print("[Large Test] Running largest_shape_area() ...")
    start = time.time()
    big_answer = largest_shape_area(big_grid)
    end = time.time()
    print(f"[Large Test] Largest area: {big_answer} (compute time: {end - start:.2f}s)")

    print("\n=== Test Runner Finished ===")


# Standard Python entry point guard to run main() when executed as a script
if __name__ == "__main__":
    main()