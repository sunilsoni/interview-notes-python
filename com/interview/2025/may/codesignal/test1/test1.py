from random import randint
from typing import List

# ---------- core solution ----------
def solution(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0

    n, m = len(matrix), len(matrix[0])
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    best = 0

    # expected value at step k
    def expected(k: int) -> int:
        if k == 0:
            return 1
        return 2 if k % 2 else 0

    for r in range(n):
        for c in range(m):
            if matrix[r][c] != 1:
                continue                        # must start with 1
            for dr, dc in directions:
                k, x, y = 0, r, c
                while 0 <= x < n and 0 <= y < m and matrix[x][y] == expected(k):
                    # check if current cell is on a border
                    on_border = x in (0, n - 1) or y in (0, m - 1)
                    # look ahead
                    nx, ny = x + dr, y + dc
                    # if next step is outside, current cell is the last one
                    if not (0 <= nx < n and 0 <= ny < m):
                        if on_border:
                            best = max(best, k + 1)
                        break
                    # if next step breaks, decide if current cell finishes on border
                    if matrix[nx][ny] != expected(k + 1):
                        if on_border:
                            best = max(best, k + 1)
                        break
                    # otherwise continue
                    x, y, k = nx, ny, k + 1
    return best
# ---------- end core solution ----------

# ---------- simple test driver ----------
def run_tests():
    cases = [
        (
            [[0, 0, 1, 2],
             [0, 2, 2, 2],
             [2, 1, 0, 1]],
            3
        ),
        (
            [[2, 1, 2, 2, 0],
             [0, 2, 0, 2, 2],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 2, 2],
             [2, 2, 0, 2, 1],
             [0, 2, 0, 0, 2]],
            3
        ),
        (
            [[1]],
            1
        ),
        (
            [[0, 0],
             [0, 0]],
            0
        ),
    ]

    # large 100×100 stress-case: put a perfect ↘ pattern of length 100
    big = [[0]*100 for _ in range(100)]
    for i in range(100):
        big[i][i] = 1 if i == 0 else (2 if i % 2 else 0)
    cases.append((big, 100))

    # random extra cases (optional, can comment out)
    for _ in range(5):
        n, m = randint(5, 12), randint(5, 12)
        rand_matrix = [[randint(0, 2) for _ in range(m)] for _ in range(n)]
        # we do not know the expected answer; just check that the call runs
        cases.append((rand_matrix, None))

    # run and report
    for idx, (mat, expect) in enumerate(cases, 1):
        got = solution(mat)
        verdict = "PASS" if expect is None or got == expect else f"FAIL (got {got}, want {expect})"
        print(f"Test {idx}: {verdict}")

if __name__ == "__main__":
    run_tests()
