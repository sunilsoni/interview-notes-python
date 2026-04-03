"""
1. Question Details:
Calculate final discounted price of items. Each item is discounted by the first equal or lower price to its right. Print total cost and indices of items sold at full price.

2. Problem Analysis:
- Array sizes up to 10^5.
- Requires an O(N) approach to avoid Time Limit Exceeded (TLE).
- Core pattern: Next Smaller or Equal Element (NSEE).

3. Solution Design:
- Use a monotonic stack to track item indices.
- Iterate array. If current price <= price at stack top, apply discount and pop.
- Remaining indices in stack are items sold at full price.

6. Code Review:
- Time Complexity: O(N) because each element is pushed/popped at most once.
- Space Complexity: O(N) for stack and result array.
"""


def finalPrice(prices):
    stack = []
    final_prices = list(prices)

    for i, p in enumerate(prices):
        while stack and prices[stack[-1]] >= p:
            idx = stack.pop()
            final_prices[idx] -= p
        stack.append(i)

    print(sum(final_prices))
    print(*stack)


# 4 & 5. Implementation and Testing
def test_runner():
    import io
    import sys

    def run_test(test_name, prices, expected_total, expected_indices):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        finalPrice(prices)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip('\n').split('\n')
        actual_total = int(output[0])
        actual_indices = output[1].strip() if len(output) > 1 else ""

        if actual_total == expected_total and actual_indices == expected_indices:
            print(f"PASS - {test_name}")
        else:
            print(
                f"FAIL - {test_name} | Expected: {expected_total}, '{expected_indices}' | Got: {actual_total}, '{actual_indices}'")

    # Provided Sample Cases
    run_test("Sample Case 0", [5, 1, 3, 4, 6, 2], 14, "1 5")
    run_test("Sample Case 1", [1, 3, 3, 2, 5], 9, "0 3 4")
    run_test("Explanation Example", [2, 3, 1, 2, 4, 2], 8, "2 5")

    # Edge Case: All items same price
    run_test("All Same Price", [5, 5, 5, 5], 5, "3")

    # Large Data Input Case (10^5 elements)
    # Strictly decreasing array: worst-case check for naive O(N^2)
    large_prices = [10 ** 6 - i for i in range(10 ** 5)]
    # Each item discounted by next item (diff = 1), except last item
    expected_large_total = (10 ** 5 - 1) * 1 + large_prices[-1]
    run_test("Large Data (100k elements)", large_prices, expected_large_total, "99999")


if __name__ == '__main__':
    test_runner()