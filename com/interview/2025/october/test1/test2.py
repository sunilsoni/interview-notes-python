from collections import Counter
import random

def solution(a, b, queries):
    cntA = Counter(a)
    cntB = Counter(b)
    out = []
    for q in queries:
        if q[0] == 0:
            _, i, x = q
            old = a[i]
            new = old + x
            cntA[old] -= 1
            if cntA[old] == 0:
                del cntA[old]
            a[i] = new
            cntA[new] += 1
        else:
            _, x = q
            total = 0
            for vb, cb in cntB.items():
                total += cb * cntA.get(x - vb, 0)
            out.append(total)
    return out

# ----------------- simple tests and large-data test -----------------

def _naive(a, b, queries):
    a = a[:]
    out = []
    cntB = Counter(b)
    for q in queries:
        if q[0] == 0:
            a[q[1]] += q[2]
        else:
            x = q[1]
            s = 0
            for ai in a:
                s += cntB.get(x - ai, 0)
            out.append(s)
    return out

def _run_tests():
    tests = []

    # Example 1
    a = [1, 4]
    b = [1, 2, 3]
    queries = [[1, 5], [0, 0, 2], [1, 5]]
    expected = [1, 2]
    tests.append((a, b, queries, expected))

    # Example 2
    a = [2, 3]
    b = [1, 2, 2]
    queries = [[1, 4], [0, 0, 1], [1, 5]]
    expected = [3, 4]
    tests.append((a, b, queries, expected))

    # Random small tests vs naive
    random.seed(7)
    for _ in range(6):
        n = random.randint(1, 25)
        m = random.randint(1, 20)
        qn = random.randint(1, 30)
        a = [random.randint(0, 50) for _ in range(n)]
        b = [random.randint(0, 50) for _ in range(m)]
        queries = []
        for __ in range(qn):
            if random.random() < 0.4:
                i = random.randrange(n)
                x = random.randint(0, 20)
                queries.append([0, i, x])
            else:
                x = random.randint(0, 150)
                queries.append([1, x])
        expected = _naive(a, b, queries)
        tests.append((a, b, queries, expected))

    # Run tests
    for idx, (aa, bb, qq, exp) in enumerate(tests, 1):
        got = solution(aa[:], bb[:], [q[:] for q in qq])
        print("PASS" if got == exp else "FAIL")

    # Large input test (performance/shape)
    n, m, qn = 50000, 1000, 1000
    random.seed(42)
    a = [random.randint(0, 10**8) for _ in range(n)]
    b = [random.randint(0, 10**8) for _ in range(m)]
    queries = []
    for _ in range(qn):
        if random.random() < 0.3:
            i = random.randrange(n)
            x = random.randint(0, 10**5)
            queries.append([0, i, x])
        else:
            x = random.randint(0, 3 * 10**8)
            queries.append([1, x])
    out = solution(a, b, queries)
    large_ok = len(out) == sum(1 for q in queries if q[0] == 1)
    print("Large input test passed:", str(large_ok).lower())

if __name__ == "__main__":
    _run_tests()
