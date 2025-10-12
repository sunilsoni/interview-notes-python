def solution(deck):
    n = len(deck)
    if n == 0:
        return -1
    try:
        k = deck.index(1)
    except ValueError:
        return -1
    for i in range(n):
        if deck[(k + i) % n] != i + 1:
            return -1
    return k

def make_deck(n, k):
    k %= n
    a = list(range(1, n + 1))
    return a[-k:] + a[:-k]

if __name__ == "__main__":
    tests = []
    expected = []
    tests.append([1, 4, 2, 3]); expected.append(-1)
    tests.append([3, 4, 5, 1, 2]); expected.append(3)
    tests.append([1, 2, 3, 4, 5]); expected.append(0)
    tests.append([2, 3, 4, 5, 6, 1]); expected.append(5)
    tests.append([4, 1, 2, 3]); expected.append(1)
    tests.append([2, 1, 3]); expected.append(-1)
    tests.append(make_deck(7, 3)); expected.append(3)
    for i in range(len(tests)):
        print("PASS" if solution(tests[i]) == expected[i] else "FAIL")
    n = 200000
    k = 56789
    large = make_deck(n, k)
    print("Large input test passed: " + str(solution(large) == k))
    broken = large[:]
    broken[0], broken[1] = broken[1], broken[0]
    print("Large input test passed: " + str(solution(broken) == -1))
