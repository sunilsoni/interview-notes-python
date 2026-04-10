def min_router_cost(positions, num_routers):
    n = len(positions)
    if num_routers >= n:
        return 0.0

    positions.sort()

    P1 = [0.0] * (n + 1)
    P2 = [0.0] * (n + 1)
    for i in range(n):
        P1[i + 1] = P1[i] + positions[i]
        P2[i + 1] = P2[i] + positions[i] ** 2

    cost = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            count = j - i + 1
            s1 = P1[j + 1] - P1[i]
            s2 = P2[j + 1] - P2[i]
            cost[i][j] = s2 - (s1 ** 2 / count)

    dp = [[float('inf')] * (n + 1) for _ in range(num_routers + 1)]
    for r in range(num_routers + 1):
        dp[r][0] = 0.0

    for i in range(1, n + 1):
        dp[1][i] = cost[0][i - 1]

    for r in range(2, num_routers + 1):
        for i in range(r, n + 1):
            for s in range(r - 1, i):
                current_cost = dp[r - 1][s] + cost[s][i - 1]
                if current_cost < dp[r][i]:
                    dp[r][i] = current_cost

    return dp[num_routers][n]

if __name__ == '__main__':
    houses = [1, 3, 9, 12]
    K = 2
    print(min_router_cost(houses, K))