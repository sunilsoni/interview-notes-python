#!/usr/bin/env python3
"""
Problem:
  You have an m × n grid `board` with 0s (empty) and 1s (rooks).
  A rook can move horizontally or vertically only to capture another rook
  (you cannot move to an empty square). Each capture removes one rook.
  Repeat until no more captures are possible, and you reach a "peaceful state".

  Find the **minimum** number of rooks that can remain.

Key insight:
  Two rooks can ultimately merge if and only if they are in the same
  connected component when you link any two rooks sharing a row or column.
  So the answer = the number of connected components among all rooks.

Example 1:
  board = [
    [0,0,1,0],
    [1,0,1,0],
    [0,0,0,1]
  ]
  There are 4 rooks; three in one component (they share rows/cols) and one isolated.
  -> min remaining = 2

Example 2:
  board = [
    [1,0,0,1],
    [0,0,0,0],
    [1,0,0,1]
  ]
  All 4 rooks are linked (row 0, row 2, col 0, col 3), so only 1 can remain.
"""

from collections import defaultdict

class UnionFind:
    """Simple Union-Find (Disjoint Set) with path compression."""
    def __init__(self, size):
        # parent[i] = parent of i; start each node as its own parent
        self.parent = list(range(size))
    def find(self, x):
        # find root representative of x, compressing path
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, a, b):
        # merge the sets containing a and b
        rootA = self.find(a)
        rootB = self.find(b)
        if rootA != rootB:
            # attach one root to the other
            self.parent[rootB] = rootA

def find_min_rooks(board):
    """
    Given a 2D list `board` of 0s and 1s, return the minimum number
    of rooks that can remain after repeated valid captures.
    """
    # 1) Collect all rook positions and give each an index
    positions = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == 1:
                positions.append((i, j))
    n = len(positions)              # total number of rooks
    if n == 0:
        return 0                    # no rooks at all → zero remain

    # 2) Group rook indices by row and by column
    rows = defaultdict(list)        # rows[r] = list of rook-indices on row r
    cols = defaultdict(list)        # cols[c] = list of rook-indices on column c
    for idx, (r, c) in enumerate(positions):
        rows[r].append(idx)
        cols[c].append(idx)

    # 3) Initialize Union-Find over the n rooks
    uf = UnionFind(n)

    # 4) For each row, union all rooks on that row
    for rook_list in rows.values():
        # if there are k rooks in this row, link them all together
        first = rook_list[0]
        for other in rook_list[1:]:
            uf.union(first, other)

    # 5) For each column, union all rooks on that column
    for rook_list in cols.values():
        first = rook_list[0]
        for other in rook_list[1:]:
            uf.union(first, other)

    # 6) Count distinct root representatives → that's # of components
    unique_roots = {uf.find(i) for i in range(n)}
    return len(unique_roots)

if __name__ == "__main__":
    # --- Provided examples ---
    tests = [
        {
            "name": "Example1",
            "board": [
                [0,0,1,0],
                [1,0,1,0],
                [0,0,0,1]
            ],
            "expected": 2
        },
        {
            "name": "Example2",
            "board": [
                [1,0,0,1],
                [0,0,0,0],
                [1,0,0,1]
            ],
            "expected": 1
        }
    ]

    for t in tests:
        result = find_min_rooks(t["board"])
        if result == t["expected"]:
            print(f"{t['name']}: PASS")
        else:
            print(f"{t['name']}: FAIL (expected {t['expected']}, got {result})")

    # --- Large-input sanity check ---
    # One row with 1,000 rooks → they all link in row → only 1 should remain
    N = 1000
    large_board = [ [1] * N ]     # 1×1000 board, all cells are rooks
    expected = 1
    result = find_min_rooks(large_board)
    if result == expected:
        print("Large test: PASS")
    else:
        print(f"Large test: FAIL (expected {expected}, got {result})")

    # You can add more random or worst-case tests here if needed.