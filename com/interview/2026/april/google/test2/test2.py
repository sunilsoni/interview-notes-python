def getMinTime(n, d, x, y):
    p = list(range(n))
    c = n

    def find(i):
        if p[i] == i: return i
        p[i] = find(p[i])
        return p[i]

    def union(i, j):
        nonlocal c
        r1, r2 = find(i), find(j)
        if r1 != r2:
            p[r1] = r2
            c -= 1

    pts = sorted([(x[i], y[i], i) for i in range(n)])
    for i in range(n - 1):
        if pts[i][0] == pts[i + 1][0] and pts[i + 1][1] - pts[i][1] <= d:
            union(pts[i][2], pts[i + 1][2])

    pts.sort(key=lambda a: (a[1], a[0]))
    for i in range(n - 1):
        if pts[i][1] == pts[i + 1][1] and pts[i + 1][0] - pts[i][0] <= d:
            union(pts[i][2], pts[i + 1][2])

    return c


def test_solution():
    cases = [
        {"args": (4, 1, [0, 0, 1, 2], [0, 1, 0, 2]), "expected": 2},
        {"args": (4, 5, [0, 0, 1, 1], [2, 5, 5, 1]), "expected": 1},
        {"args": (3, 0, [0, 0, 1], [0, 1, 2]), "expected": 3},
        {"args": (5, 2, [0, 2, 4, 6, 8], [0, 0, 0, 0, 0]), "expected": 1},  # Chain reaction line
        {"args": (100000, 1, list(range(100000)), [0] * 100000), "expected": 1}  # Large data test
    ]

    for i, case in enumerate(cases):
        ans = getMinTime(*case["args"])
        status = "PASS" if ans == case["expected"] else f"FAIL (Got {ans}, Expected {case['expected']})"
        print(f"Test Case {i + 1}: {status}")


if __name__ == '__main__':
    test_solution()