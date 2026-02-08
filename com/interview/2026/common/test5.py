import sys

def getMinOperations(n):
    c = 0
    while n:
        if n & 1 == 0:
            n >>= 1
        else:
            n += 1 if n != 1 and (n & 3) == 3 else -1
            c += 1
    return c

def _run_tests():
    cases = [
        (5, 2),
        (21, 3),
        (7, 2),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 1),
        (8, 1),
        (15, 2),
        (9, 2),
        (10, 2),
        (12, 2),
        (14, 2),
        ((1 << 60) - 1, 2),
    ]
    ok = True
    for n, exp in cases:
        got = getMinOperations(n)
        pass_ = got == exp
        ok &= pass_
        print(("PASS" if pass_ else "FAIL"), n, got, exp)
    if ok:
        print("ALL_PASS")

if __name__ == "__main__":
    data = sys.stdin.read().strip().split()
    if data:
        print(getMinOperations(int(data[0])))
    else:
        _run_tests()
