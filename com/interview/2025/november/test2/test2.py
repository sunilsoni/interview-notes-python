import sys
import random
import time
from collections import defaultdict, deque

def palindromePaths(tree_nodes, tree_from, tree_to, arr, queries):
    sys.setrecursionlimit(1 << 25)
    n = tree_nodes
    g = [[] for _ in range(n)]
    for u, v in zip(tree_from, tree_to):
        g[u].append(v)
        g[v].append(u)

    def bit(c):
        return 1 << (ord(c) - 97)

    parent = [-1] * n
    order = []
    stack = [0]
    parent[0] = -2
    while stack:
        u = stack.pop()
        order.append(u)
        for v in g[u]:
            if parent[v] == -1:
                parent[v] = u
                stack.append(v)
    parent[0] = -1

    s = [0] * n
    sp = [0] * n
    for u in order:
        p = parent[u]
        if p != -1:
            s[u] = s[p] ^ bit(arr[u])
            sp[u] = s[p]
        else:
            s[u] = bit(arr[u])
            sp[u] = 0

    cnt = defaultdict(int)
    ans = [0] * n

    def dfs(u, p):
        cnt[sp[u]] += 1
        total = cnt[s[u]]
        x = s[u]
        for k in range(26):
            total += cnt[x ^ (1 << k)]
        ans[u] = total
        for v in g[u]:
            if v == p:
                continue
            dfs(v, u)
        cnt[sp[u]] -= 1

    dfs(0, -1)
    return [ans[q] for q in queries]


# ---------- Tests ----------

def _naive(tree_nodes, tree_from, tree_to, arr, queries):
    n = tree_nodes
    g = [[] for _ in range(n)]
    for u, v in zip(tree_from, tree_to):
        g[u].append(v)
        g[v].append(u)
    parent = [-1] * n
    stack = [0]
    parent[0] = -2
    while stack:
        u = stack.pop()
        for v in g[u]:
            if parent[v] == -1:
                parent[v] = u
                stack.append(v)
    parent[0] = -1

    def bit(c):
        return 1 << (ord(c) - 97)

    res = []
    for q in queries:
        mask = 0
        cur = q
        cnt = 0
        while cur != -1:
            mask ^= bit(arr[cur])
            if mask & (mask - 1) == 0:
                cnt += 1
            cur = parent[cur]
        res.append(cnt)
    return res

def _assert_equal(name, a, b):
    ok = a == b
    print(f"{name}: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print("  expected:", a)
        print("  actual  :", b)

def _run_samples():
    # Sample Case 0
    n = 4
    arr = ['a','b','a','a']
    f = [0,1,0]
    t = [1,3,2]
    queries = [1,2]
    exp = [1,2]
    _assert_equal("Sample 0", exp, palindromePaths(n, f, t, arr, queries))

    # Sample Case 1
    n = 7
    arr = ['a','b','c','a','c','b','c']
    f = [0,1,2,2,4,4]
    t = [1,2,3,4,5,6]
    queries = [6,5,3]
    exp = [3,4,1]
    _assert_equal("Sample 1", exp, palindromePaths(n, f, t, arr, queries))

    # Extra example from prompt text (z a a a)
    n = 4
    arr = ['z','a','a','a']
    f = [0,0,1]
    t = [1,2,3]
    queries = [3]
    exp = [3]
    _assert_equal("Example z/a", exp, palindromePaths(n, f, t, arr, queries))

def _run_random_correctness():
    random.seed(0)
    for tc in range(1, 51):
        n = random.randint(1, 60)
        f, t = [], []
        for i in range(1, n):
            p = random.randint(0, i - 1)
            f.append(p)
            t.append(i)
        arr = [chr(97 + random.randint(0, 25)) for _ in range(n)]
        m = random.randint(1, 80)
        queries = [random.randint(0, n - 1) for _ in range(m)]
        exp = _naive(n, f, t, arr, queries)
        got = palindromePaths(n, f, t, arr, queries)
        _assert_equal(f"Random {tc:02d}", exp, got)

def _run_large_performance():
    random.seed(1)
    n = 100000
    f, t = [], []
    for i in range(1, n):
        p = random.randint(0, i - 1)
        f.append(p)
        t.append(i)
    arr = [chr(97 + random.randint(0, 25)) for _ in range(n)]
    m = 100000
    queries = [random.randint(0, n - 1) for _ in range(m)]
    t0 = time.time()
    _ = palindromePaths(n, f, t, arr, queries)
    t1 = time.time()
    print(f"Large Test (n={n}, m={m}): PASS in {t1 - t0:.2f}s")

if __name__ == "__main__":
    _run_samples()
    _run_random_correctness()
    _run_large_performance()
