from bisect import bisect_right, bisect_left
import random, time

# ---------------- core function ----------------
def solution(lamps, points):
    """
    lamps  : List[List[int]]  -- segments [l, r]  (inclusive)
    points : List[int]        -- query coordinates
    returns: List[int]        -- lamps illuminating each point
    """
    # separate, then sort, all starts and ends
    starts = sorted(l[0] for l in lamps)
    ends   = sorted(l[1] for l in lamps)

    ans = []
    for p in points:
        # how many segments start at or before p
        left  = bisect_right(starts, p)
        # how many segments end  before p   (strict)
        right = bisect_left(ends, p)
        ans.append(left - right)
    return ans
# ------------------------------------------------


# ----------------- simple tests -----------------
def run_tests():
    tests = []

    # example from the statement
    tests.append((
        [[1, 7], [5, 11], [7, 9]],
        [7, 1, 5, 10, 9, 15],
        [3, 1, 2, 1, 2, 0]
    ))

    # single lamp, multiple points
    tests.append(([[2, 4]], [1, 2, 3, 4, 5], [0, 1, 1, 1, 0]))

    # edges touching
    tests.append(([[5, 5], [1, 10]], [5], [2]))

    # large random stress – should finish well under the 4 s limit
    N, M = 100_000, 100_000
    lamps = [[random.randint(1, 100_000), 0] for _ in range(N)]
    for seg in lamps:
        seg[1] = random.randint(seg[0], 100_000)
    points = [random.randint(1, 100_000) for _ in range(M)]
    tests.append((lamps, points, None))   # expected unknown, just check runtime

    # ----- run -----
    for idx, (ls, ps, expected) in enumerate(tests, 1):
        start = time.perf_counter()
        out = solution(ls, ps)
        elapsed = time.perf_counter() - start

        if expected is not None:
            ok = out == expected
            print(f"Test {idx}: {'PASS' if ok else 'FAIL'} ({elapsed:.3f}s)")
            if not ok:
                print(f" expected: {expected}\n got     : {out}")
                return
        else:
            print(f"Stress test {idx}: completed in {elapsed:.3f}s (no crashes)")

if __name__ == "__main__":
    run_tests()
