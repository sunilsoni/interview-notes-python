"""
Question Details: Minimum Reversal
Optimize a directed graph representing a neural network by selecting a root node
that minimizes the number of edge reversals needed. The graph has g_nodes nodes
numbered from 1 to g_nodes and g_nodes-1 edges.

Constraints:
- 2 <= g_nodes <= 10^5
- 1 <= g_from[i], g_to[i] <= g_nodes
- g_from[i] != g_to[i]
"""

from collections import deque


def getMinInversions(g_nodes, g_from, g_to):
    adj = [[] for _ in range(g_nodes + 1)]
    for u, v in zip(g_from, g_to):
        adj[u].append((v, 0))
        adj[v].append((u, 1))

    q = deque([1])
    visited = {1}
    initial_cost = 0

    while q:
        u = q.popleft()
        for v, cost in adj[u]:
            if v not in visited:
                visited.add(v)
                initial_cost += cost
                q.append(v)

    costs = {1: initial_cost}
    q = deque([1])
    visited = {1}
    min_cost = initial_cost

    while q:
        u = q.popleft()
        for v, cost in adj[u]:
            if v not in visited:
                visited.add(v)
                costs[v] = costs[u] + (1 if cost == 0 else -1)
                if costs[v] < min_cost:
                    min_cost = costs[v]
                q.append(v)

    return min_cost


def run_tests():
    test_cases = [
        {
            "name": "Image Example",
            "g_nodes": 4,
            "g_from": [1, 2, 3],
            "g_to": [4, 4, 4],
            "expected": 2
        },
        {
            "name": "Sample Case 0",
            "g_nodes": 3,
            "g_from": [2, 2],
            "g_to": [1, 3],
            "expected": 0
        },
        {
            "name": "Sample Case 1",
            "g_nodes": 4,
            "g_from": [1, 1, 4],
            "g_to": [3, 2, 2],
            "expected": 1
        }
    ]

    # Large Data Input Case (10^5 nodes forming a straight line 1->2->...->100000)
    large_nodes = 100000
    large_from = list(range(1, large_nodes))
    large_to = list(range(2, large_nodes + 1))
    test_cases.append({
        "name": "Large Data Chain",
        "g_nodes": large_nodes,
        "g_from": large_from,
        "g_to": large_to,
        "expected": 0
    })

    # Large Data Input Case 2 (Star Graph, edges pointing to center)
    star_nodes = 100000
    star_from = list(range(2, star_nodes + 1))
    star_to = [1] * (star_nodes - 1)
    test_cases.append({
        "name": "Large Data Star (Inward)",
        "g_nodes": star_nodes,
        "g_from": star_from,
        "g_to": star_to,
        "expected": star_nodes - 2  # Rooting at anything but 1 requires changing N-2 edges
    })

    all_passed = True
    for tc in test_cases:
        result = getMinInversions(tc["g_nodes"], tc["g_from"], tc["g_to"])
        status = "PASS" if result == tc["expected"] else "FAIL"
        print(f"[{status}] {tc['name']} | Expected: {tc['expected']} | Got: {result}")
        if status == "FAIL":
            all_passed = False

    print("\nOVERALL STATUS:", "ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED")


if __name__ == '__main__':
    run_tests()