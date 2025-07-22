#!/usr/bin/env python3
"""
Restore Minimum Server Configuration

Given a corrupted configuration string config and integers x, y,
reconstruct the original final configuration string (digits 0–9)
with the minimum possible decimal value from which config can be obtained
by deleting some digits. Return "-1" if impossible.

### Example 1:
Input:
    config = "324"
    x = 2
    y = 3
Output:
    36924
Explanation:
    0 + y = 3 → 3
    3 + x = 5 → 5 → 6
    6 + y = 9 → 9
    9 + x = 11 → 1
    11 + y = 14 → 4
    Final = 36924, and "324" is a subsequence.

### Example 2:
Input:
    config = "521"
    x = 5
    y = 5
Output:
    -1
Explanation:
    Only digits 0 and 5 are generated, so 2 and 1 are impossible.
"""

from collections import deque
import time
import random

def missingDigits(config, x, y):
    nbr = {}
    for u in range(10):
        a = (u + x) % 10
        b = (u + y) % 10
        nbr[u] = [a] if a == b else sorted([a, b])
    paths = [[None]*10 for _ in range(10)]
    for u in range(10):
        seen = [False]*10
        seen[u] = True
        paths[u][u] = []
        dq = deque()
        for v in nbr[u]:
            if not seen[v]:
                seen[v] = True
                paths[u][v] = [v]
                dq.append(v)
        while dq:
            cur = dq.popleft()
            for v in nbr[cur]:
                if not seen[v]:
                    seen[v] = True
                    paths[u][v] = paths[u][cur] + [v]
                    dq.append(v)
    if not config:
        return ""
    seq = []
    first = int(config[0])
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
    return "".join(map(str, seq))

def main():
    tests = [
        ("324", 2, 3, "36924"),
        ("521", 5, 5, "-1"),
        ("27", 2, 3, "247"),
    ]
    for i, (cfg, x, y, exp) in enumerate(tests, 1):
        res = missingDigits(cfg, x, y)
        status = "PASS" if res == exp else "FAIL"
        print(f"Test {i}: {status} (got={res}, expected={exp})")
    # large random test
    x, y = 3, 7
    cur = 0
    cfg_list = []
    for _ in range(100000):
        op = random.choice([x, y])
        cur = (cur + op) % 10
        cfg_list.append(str(cur))
    cfg = "".join(cfg_list)
    t0 = time.time()
    out = missingDigits(cfg, x, y)
    t1 = time.time()
    print(f"Large test: len(config)={len(cfg)}, len(output)={len(out)}, time={(t1-t0):.3f}s")

if __name__ == "__main__":
    main()