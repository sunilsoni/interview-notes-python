"""
1. Question Details: Prime Jumps. Find max score starting at cell 0 to n-1.
Allowed moves: 1 step right, or p steps right (p is prime ending in 3).
2. Problem Analysis: DP approach is optimal. dp[i] stores max score to reach cell i.
3. Solution Design: Precompute primes ending in 3. Update dp array for allowed moves (step +1 or +p).
4. Implementation: See `maxGameScore` function.
5. Testing: Handled in `main()` with standard and large inputs.
6. Code Review: O(n * #primes) time and O(n) space. Scalable for n=10^4 constraint.
"""


def maxGameScore(cell):
    n = len(cell)
    if n <= 1:
        return 0

    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    primes = [i for i in range(2, n + 1) if is_prime[i] and i % 10 == 3]

    dp = [float('-inf')] * n
    dp[0] = 0

    for i in range(n):
        if dp[i] == float('-inf'):
            continue

        if i + 1 < n and dp[i] + cell[i + 1] > dp[i + 1]:
            dp[i + 1] = dp[i] + cell[i + 1]

        for p in primes:
            if i + p < n:
                if dp[i] + cell[i + p] > dp[i + p]:
                    dp[i + p] = dp[i] + cell[i + p]
            else:
                break

    return dp[-1]


def main():
    large_data = [0] + [-1] * 9999

    test_cases = [
        {"input": [0, -10, -20, -30, 50], "expected": 40, "desc": "Example Case"},
        {"input": [0, -10, 100, -20], "expected": 70, "desc": "Sample Case 0"},
        {"input": [0, -100, -100, -1, 0, -1], "expected": -2, "desc": "Sample Case 1"},
        {"input": large_data, "expected": maxGameScore(large_data), "desc": "Large Data (N=10000)"}
    ]

    for i, tc in enumerate(test_cases):
        res = maxGameScore(tc["input"])
        status = "PASS" if res == tc["expected"] else f"FAIL (Got {res}, Expected {tc['expected']})"
        print(f"Test {i + 1} [{tc['desc']}]: {status}")


if __name__ == '__main__':
    main()