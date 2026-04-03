"""
Problem Details:
Name: Minimum Reversal
Description: Optimize a directed graph (n nodes, n-1 edges) by selecting a root node that minimizes
the number of edge reversals needed to make all edges flow away from the root.
Returns: The minimum number of edges that must be inverted.
Constraints: 2 <= g_nodes <= 10^5, 1 <= g_from[i], g_to[i] <= g_nodes, g_from[i] != g_to[i]
"""

from collections import deque


def getMinInversions(g_nodes, g_from, g_to):
    adj = [[] for _ in range(g_nodes + 1)]

    for u, v in zip(g_from, g_to):
        adj[u].append((v, 0))  # 0 indicates original direction
        adj[v].append((u, 1))  # 1 indicates inverted direction

    visited = [False] * (g_nodes + 1)
    q = deque([1])
    visited[1] = True
    initial_cost = 0

    # First BFS to calculate the cost if node 1 is the root
    while q:
        curr = q.popleft()
        for nxt, weight in adj[curr]:
            if not visited[nxt]:
                visited[nxt] = True
                initial_cost += weight
                q.append(nxt)

    ans = initial_cost
    q = deque([(1, initial_cost)])
    visited = [False] * (g_nodes + 1)
    visited[1] = True

    # Second BFS to calculate the cost for all other nodes as roots
    while q:
        curr, cost = q.popleft()
        ans = min(ans, cost)

        for nxt, weight in adj[curr]:
            if not visited[nxt]:
                visited[nxt] = True
                # Re-rooting logic: +1 if moving along original edge, -1 if moving along inverted edge
                nxt_cost = cost + 1 if weight == 0 else cost - 1
                q.append((nxt, nxt_cost))
    return ans


if __name__ == "__main__":
    # Test Cases
    test_cases = [
        {
            "desc": "Screenshot Example 1",
            "g_nodes": 4,
            "g_from": [1, 2, 3],
            "g_to": [4, 4, 4],
            "expected": 2
        },
        {
            "desc": "Screenshot Sample Case 0",
            "g_nodes": 3,
            "g_from": [2, 2],
            "g_to": [1, 3],
            "expected": 0
        },
        {
            "desc": "Screenshot Sample Case 1",
            "g_nodes": 4,
            "g_from": [1, 1, 4],
            "g_to": [3, 2, 2],
            "expected": 1
        },
        {
            "desc": "Large Data: Straight Line Graph (1->2->3...->100000)",
            "g_nodes": 100000,
            "g_from": list(range(1, 100000)),
            "g_to": list(range(2, 100001)),
            "expected": 0
        },
        {
            "desc": "Large Data: Star Graph (All nodes pointing to 1)",
            "g_nodes": 100000,
            "g_from": list(range(2, 100001)),
            "g_to": [1] * 99999,
            "expected": 0
        }
    ]

    for i, tc in enumerate(test_cases):
        result = getMinInversions(tc["g_nodes"], tc["g_from"], tc["g_to"])
        if result == tc["expected"]:
            print(f"Test Case {i} ({tc['desc']}): PASS")
        else:
            print(f"Test Case {i} ({tc['desc']}): FAIL (Expected {tc['expected']}, Got {result})")