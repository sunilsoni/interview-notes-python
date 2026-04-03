"""
1. Question Details: Maximize the final throughput of an n-service data pipeline given a scaling budget.
2. Problem Analysis: Since services are in series, the overall throughput is bottlenecked by the minimum throughput among all services. The goal is to maximize this minimum throughput.
3. Solution Design: Use Binary Search on the answer. For a target throughput, calculate the required scale factor for each service. If the total scaling cost is within the budget, the target is feasible.
4. Implementation: Binary search range from min(throughput) to a safe upper bound (10^15).
5. Testing: Simple main method provided testing sample cases and large data limits.
6. Code Review: O(N log(Max_Throughput)) time complexity, O(1) space. Minimalistic and robust.
"""


def getMaximumThroughput(throughput, scalingCost, budget):
    low, high = min(throughput), 10 ** 15
    ans = low

    while low <= high:
        mid = (low + high) // 2
        cost = 0

        for t, c in zip(throughput, scalingCost):
            if mid > t:
                cost += ((mid - 1) // t) * c
                if cost > budget:
                    break

        if cost <= budget:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1

    return ans


if __name__ == '__main__':
    # Test cases: (throughput, scalingCost, budget, expected_output)
    tests = [
        ([4, 2, 7], [3, 5, 6], 32, 10),
        ([3, 2, 5], [2, 5, 10], 28, 6),
        ([7, 3, 4, 6], [2, 5, 4, 3], 25, 9),
        ([1], [1], 10 ** 9, 10 ** 9 + 1),  # Large budget edge case
        ([10 ** 7] * 10 ** 5, [200] * 10 ** 5, 10 ** 9, 510000000)  # Large array & max values edge case
    ]

    for i, (t, c, b, expected) in enumerate(tests):
        result = getMaximumThroughput(t, c, b)
        status = "PASS" if result == expected else f"FAIL (Expected {expected}, Got {result})"
        print(f"Test {i + 1}: {status}")