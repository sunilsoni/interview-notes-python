#!/usr/bin/env python3
"""
Problem explanation and examples...
"""

from collections import defaultdict


class UnionFind:
    """Simple Union-Find (Disjoint Set) with path compression."""

    def __init__(self, size):
        # Initialize each element as its own parent (each element starts in its own set)
        self.parent = list(range(size))  # [0,1,2,3,...,size-1]

    def find(self, x):
        # Find the root representative of element x
        # Uses path compression: makes all nodes in path point directly to root
        if self.parent[x] != x:  # If x is not its own parent
            self.parent[x] = self.find(self.parent[x])  # Recursively find root and compress
        return self.parent[x]

    def union(self, a, b):
        # Merge the sets containing elements a and b
        rootA = self.find(a)  # Find root of a's set
        rootB = self.find(b)  # Find root of b's set
        if rootA != rootB:  # If they're not already in same set
            self.parent[rootB] = rootA  # Make rootA the parent of rootB


def find_min_rooks(board):
    # Step 1: Find all rook positions
    positions = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 1:  # If there's a rook
                positions.append((i, j))  # Store its coordinates
    n = len(positions)  # Total number of rooks
    if n == 0:
        return 0  # Edge case: no rooks on board

    # Step 2: Group rooks by their rows and columns
    rows = defaultdict(list)  # Dictionary: row_number → list of rook indices
    cols = defaultdict(list)  # Dictionary: col_number → list of rook indices
    for idx, (r, c) in enumerate(positions):
        rows[r].append(idx)  # Add rook index to its row group
        cols[c].append(idx)  # Add rook index to its column group

    # Step 3: Create UnionFind structure
    uf = UnionFind(n)  # Initialize with n rooks

    # Step 4: Connect rooks in same row
    for rook_list in rows.values():
        first = rook_list[0]  # Take first rook in row
        for other in rook_list[1:]:  # Connect it to all others in same row
            uf.union(first, other)

    # Step 5: Connect rooks in same column
    for rook_list in cols.values():
        first = rook_list[0]  # Take first rook in column
        for other in rook_list[1:]:  # Connect it to all others in same column
            uf.union(first, other)

    # Step 6: Count unique components
    unique_roots = {uf.find(i) for i in range(n)}  # Set of all root representatives
    return len(unique_roots)  # Number of connected components


if __name__ == "__main__":
    # Test cases...
    # Each test case checks if actual output matches expected output
    tests = [
        {
            "name": "Example1",
            "board": [[0, 0, 1, 0], [1, 0, 1, 0], [0, 0, 0, 1]],
            "expected": 2
        },
        # ... more test cases ...
    ]

    # Run tests and print results
    for t in tests:
        result = find_min_rooks(t["board"])
        if result == t["expected"]:
            print(f"{t['name']}: PASS")
        else:
            print(f"{t['name']}: FAIL (expected {t['expected']}, got {result})")

    # Large-scale test with 1000 rooks in one row
    N = 1000
    large_board = [[1] * N]  # Create board with 1000 connected rooks
    expected = 1
    result = find_min_rooks(large_board)
    if result == expected:
        print("Large test: PASS")
    else:
        print(f"Large test: FAIL (expected {expected}, got {result})")
