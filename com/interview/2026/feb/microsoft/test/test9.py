def getMinInversions(g_nodes, g_from, g_to):
    adj = [[] for _ in range(g_nodes + 1)]
    for u, v in zip(g_from, g_to):
        adj[u].append((v, 0))
        adj[v].append((u, 1))

    q = [1]
    visited = [False] * (g_nodes + 1)
    visited[1] = True
    edges = []
    initial_cost = 0
    head = 0

    while head < len(q):
        u = q[head]
        head += 1
        for v, c in adj[u]:
            if not visited[v]:
                visited[v] = True
                initial_cost += c
                edges.append((u, v, c))
                q.append(v)

    ans = [0] * (g_nodes + 1)
    ans[1] = initial_cost

    for u, v, c in edges:
        ans[v] = ans[u] + 1 if c == 0 else ans[u] - 1

    return min(ans[1:])


if __name__ == '__main__':
    def run_test(name, g_nodes, g_from, g_to, expected):
        try:
            res = getMinInversions(g_nodes, g_from, g_to)
            if res == expected:
                print(f"Test {name}: PASS")
            else:
                print(f"Test {name}: FAIL (Expected {expected}, Got {res})")
        except Exception as e:
            print(f"Test {name}: FAIL with Exception -> {e}")


    # Provided Sample Cases
    run_test("Sample 0", 3, [2, 2], [1, 3], 0)
    run_test("Sample 1", 4, [1, 1, 4], [3, 2, 2], 1)
    run_test("Example", 4, [1, 2, 3], [4, 4, 4], 2)

    # Large Data Case 1: Sequential directed path (1->2->3...->100000)
    n = 100000
    run_test("Large Sequential Forward", n, list(range(1, n)), list(range(2, n + 1)), 0)

    # Large Data Case 2: Sequential directed backwards (100000->99999->...->1)
    run_test("Large Sequential Backward", n, list(range(2, n + 1)), list(range(1, n)), 0)

    # Large Data Case 3: Star graph pointing outwards from center node 1
    run_test("Large Star Outward", n, [1] * (n - 1), list(range(2, n + 1)), 0)

    # Large Data Case 4: Star graph pointing inwards to center node 1
    run_test("Large Star Inward", n, list(range(2, n + 1)), [1] * (n - 1), 0)