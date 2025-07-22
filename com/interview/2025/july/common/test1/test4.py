from collections import deque
from typing import List, Tuple

def missingDigits(config: str, x: int, y: int) -> str:
    n = len(config)
    # next_state[(i, d)] = (i', d'), but we compute on the fly
    # BFS over (matched_index, current_digit)
    start = (0, 0)
    queue = deque([start])
    visited = [[False]*10 for _ in range(n+1)]
    visited[0][0] = True
    prev = {}
    while queue:
        i, d = queue.popleft()
        if i == n:
            # reconstruct
            seq = []
            cur = (i, d)
            while cur in prev:
                p, digit = prev[cur]
                seq.append(str(digit))
                cur = p
            return "".join(reversed(seq))
        for add in sorted((x, y)):
            nd = (d + add) % 10
            ni = i + (i < n and config[i] == str(nd))
            if not visited[ni][nd]:
                visited[ni][nd] = True
                prev[(ni, nd)] = ((i, d), nd)
                queue.append((ni, nd))
    return "-1"

if __name__ == "__main__":
    test_cases = [
        # Example 1
        {"config": "324", "x": 2, "y": 3, "expected": "36924"},
        # Example 2
        {"config": "521", "x": 5, "y": 5, "expected": "-1"},
        # Single digit
        {"config": "0", "x": 1, "y": 2, "expected": "10"},
        # Repeated pattern
        {"config": "1212", "x": 1, "y": 1, "expected": "01212"},
        # Impossible
        {"config": "7", "x": 2, "y": 4, "expected": "-1"},
    ]

    for idx, tc in enumerate(test_cases, 1):
        res = missingDigits(tc["config"], tc["x"], tc["y"])
        status = "PASS" if res == tc["expected"] else "FAIL"
        print(f"Test {idx}: {status} (got={res}, expected={tc['expected']})")

    # Large test for performance
    # config of 1000 zeros, x=10-1=9,y=1 generates 0 every 10 steps
    large_config = "0" * 1000
    res = missingDigits(large_config, 9, 1)
    expected = "0" + "1" * 1000  # 0->1->... cycles back to 0
    status = "PASS" if res.endswith("0") and len(res) >= 1001 else "FAIL"
    print(f"Large test: {status} (length={len(res)})")
