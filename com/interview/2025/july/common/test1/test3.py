#!/usr/bin/env python3
"""
Given a corrupted configuration string config and integers x, y,
reconstruct the original final configuration (string of recorded unit digits)
with the minimum possible decimal value from which config can be obtained
by removing digits. Return "-1" if impossible.
"""

from collections import deque
import random
import time

def missingDigits(config, x, y):
    # build neighbor map for mod-10 graph
    nbr = {}
    for u in range(10):
        a = (u + x) % 10
        b = (u + y) % 10
        if a == b:
            nbr[u] = [a]
        else:
            nbr[u] = sorted([a, b])
    # precompute lexicographically smallest shortest paths for each start u to every v
    paths = [[None] * 10 for _ in range(10)]
    for u in range(10):
        visited = [False] * 10
        visited[u] = True
        paths[u][u] = []
        dq = deque()
        # first layer
        for v in nbr[u]:
            if not visited[v]:
                visited[v] = True
                paths[u][v] = [v]
                dq.append(v)
        # BFS
        while dq:
            cur = dq.popleft()
            for v in nbr[cur]:
                if not visited[v]:
                    visited[v] = True
                    paths[u][v] = paths[u][cur] + [v]
                    dq.append(v)
    # reconstruct
    if not config:
        return ""
    first = int(config[0])
    seq = []
    p0 = paths[0][first]
    if p0 is None:
        return "-1"
    seq.extend(p0)
    cur = first
    for ch in config[1:]:
        t = int(ch)
        p = paths[cur][t]
        if p is None:
            return "-1"
        seq.extend(p)
        cur = t
    return ''.join(str(d) for d in seq)

def main():
    tests = [
        ("324", 2, 3, "36924"),
        ("521", 5, 5, "-1"),
        ("27", 2, 3, "247"),
        ("57", 5, 7, "57"),
    ]
    all_pass = True
    for i, (cfg, x, y, exp) in enumerate(tests, 1):
        res = missingDigits(cfg, x, y)
        status = "PASS" if res == exp else "FAIL"
        print(f"Test {i}: {status} (got={res}, expected={exp})")
        if res != exp:
            all_pass = False
    print("All tests passed." if all_pass else "Some tests failed.")
    # large random test
    x, y = 3, 7
    cur = 0
    cfg_list = []
    for _ in range(100000):
        op = random.choice([x, y])
        cur = (cur + op) % 10
        cfg_list.append(str(cur))
    cfg = ''.join(cfg_list)
    t0 = time.time()
    out = missingDigits(cfg, x, y)
    t1 = time.time()
    print(f"Large test: len(config)={len(cfg)}, len(output)={len(out)}, time={(t1-t0):.3f}s")

if __name__ == "__main__":
    main()