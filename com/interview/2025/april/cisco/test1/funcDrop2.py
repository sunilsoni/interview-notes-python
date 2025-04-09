from collections import defaultdict

def funcDrop(xCoordinate, yCoordinate):
    """
    Returns the maximum number of distinct drop‑points
    that lie on a single vertical (x = c) or horizontal (y = c) line.
    A valid path needs at least two different coordinates.
    """
    # Build:  x -> set of all y's on that x
    #         y -> set of all x's on that y
    x_to_ys = defaultdict(set)
    y_to_xs = defaultdict(set)

    for x, y in zip(xCoordinate, yCoordinate):
        x_to_ys[x].add(y)
        y_to_xs[y].add(x)

    # Largest vertical & horizontal path lengths
    max_vert = max((len(ys) for ys in x_to_ys.values()), default=0)
    max_horz = max((len(xs) for xs in y_to_xs.values()), default=0)

    best = max(max_vert, max_horz)
    return best if best >= 2 else 0  # 0 when no valid path


def main():
    # ---- read one test case from STDIN ----
    n = int(input().strip())
    x_vals = list(map(int, input().split()))
    m = int(input().strip())
    y_vals = list(map(int, input().split()))
    print(funcDrop(x_vals, y_vals))


# ------------- simple test‑runner -------------
def run_tests():
    tests = [
        # sample case
        ([2, 3, 2, 4, 2], [2, 2, 6, 5, 8], 3),
        # only vertical line
        ([5, 5], [1, 2], 2),
        # duplicates on same point – no valid path
        ([1, 1, 2], [1, 1, 2], 0),
        # all unique coordinates – no valid path
        ([1, 2, 3], [4, 5, 6], 0),
        # horizontal best
        ([1, 2, 3, 4], [7, 7, 7, 1], 3),
    ]

    passed = 0
    for idx, (xs, ys, exp) in enumerate(tests, 1):
        got = funcDrop(xs, ys)
        status = "PASS" if got == exp else "FAIL"
        print(f"Test {idx}: {status}  |  expected {exp}  got {got}")
        if status == "PASS":
            passed += 1
    print(f"\nSummary: {passed}/{len(tests)} tests passed")


if __name__ == "__main__":
    # comment/uncomment as needed
    # main()          # for online judge
    run_tests()       # local quick check
