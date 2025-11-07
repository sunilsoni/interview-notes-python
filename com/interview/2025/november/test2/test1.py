from bisect import bisect_right
import random
import time


def findMaximumValue(prices, pos, amount):
    n = len(prices)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + prices[i]
    ans = []
    for p, a in zip(pos, amount):
        t = prefix[p - 1] + a
        idx = bisect_right(prefix, t) - 1
        ans.append(max(0, idx - (p - 1)))
    return ans


def _naive(prices, pos, amount):
    # for small arrays: pick greedily from pos forward (works because non-decreasing)
    res = []
    for p, a in zip(pos, amount):
        s = 0
        c = 0
        for v in prices[p - 1:]:
            if s + v <= a:
                s += v
                c += 1
            else:
                break
        res.append(c)
    return res


def _assert_equal(name, expected, actual):
    ok = expected == actual
    print(f"{name}: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  expected:", expected)
        print("  actual  :", actual)


def _run_samples():
    prices = [1, 2, 3, 4, 5]
    pos = [1, 3]
    amount = [4, 14]
    expected = [2, 3]
    _assert_equal("Sample 0", expected, findMaximumValue(prices, pos, amount))

    prices = [1, 2, 2, 2, 3]
    pos = [2, 5]
    amount = [5, 2]
    expected = [2, 0]
    _assert_equal("Sample 1", expected, findMaximumValue(prices, pos, amount))

    prices = [3, 4, 5, 5, 7]
    pos = [2, 1, 5]
    amount = [10, 24, 5]
    expected = [2, 5, 0]
    _assert_equal("Example", expected, findMaximumValue(prices, pos, amount))


def _run_edge_tests():
    _assert_equal(
        "Edge: single item, enough",
        [1],
        findMaximumValue([5], [1], [6]),
    )
    _assert_equal(
        "Edge: single item, not enough",
        [0],
        findMaximumValue([5], [1], [4]),
    )
    _assert_equal(
        "Edge: zero budget",
        [0, 0],
        findMaximumValue([1, 1, 1], [1, 2], [0, 0]),
    )
    _assert_equal(
        "Edge: start at end",
        [1],
        findMaximumValue([1, 2, 3], [3], [3]),
    )
    _assert_equal(
        "Edge: large amount buys all",
        [3],
        findMaximumValue([2, 2, 2], [1], [100]),
    )


def _run_random_correctness_tests():
    random.seed(0)
    for tc in range(1, 51):
        n = random.randint(1, 60)
        arr = sorted(random.randint(1, 20) for _ in range(n))
        q = random.randint(1, 80)
        pos = [random.randint(1, n) for _ in range(q)]
        amount = [random.randint(0, 200) for _ in range(q)]
        exp = _naive(arr, pos, amount)
        got = findMaximumValue(arr, pos, amount)
        name = f"Random {tc:02d}"
        _assert_equal(name, exp, got)


def _run_large_performance_test():
    random.seed(1)
    n = 100000
    base = 1
    prices = []
    for _ in range(n):
        base += random.randint(0, 2)  # non-decreasing
        prices.append(base)
    q = 100000
    pos = [random.randint(1, n) for _ in range(q)]
    amount = [random.randint(0, 10**12) for _ in range(q)]
    t0 = time.time()
    _ = findMaximumValue(prices, pos, amount)
    t1 = time.time()
    print(f"Large Test (n={n}, q={q}): PASS in {t1 - t0:.2f}s")


if __name__ == "__main__":
    _run_samples()
    _run_edge_tests()
    _run_random_correctness_tests()
    _run_large_performance_test()
