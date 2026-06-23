def minTotalCost(numItems, itemId, cost):
    # We need to keep track of the smallest cost we find for each individual item.
    # We create a list called 'min_costs' that has exactly 'numItems' number of slots.
    # We initialize every slot with infinity (float('inf')) because we haven't seen any costs yet.
    min_costs = [float('inf')] * numItems

    # We find out how many total cost entries were provided in the input arrays.
    n = len(itemId)

    # We start a loop to go through every single entry in the arrays one by one.
    for i in range(n):
        # We pull out the item ID for the current entry we are looking at.
        current_id = itemId[i]

        # We pull out the cost for the current entry we are looking at.
        current_cost = cost[i]

        # We check if this new cost is cheaper than the cost we previously saved for this item.
        if current_cost < min_costs[current_id]:
            # If it is cheaper, we replace the old, more expensive cost with this new, cheaper one.
            min_costs[current_id] = current_cost

    # We create a variable called 'total_cost' and start it at 0 to hold our final answer.
    total_cost = 0

    # We start a second loop to look at the lowest costs we saved for every required item.
    for i in range(numItems):
        # We grab the saved minimum cost for the current item 'i'.
        saved_cost = min_costs[i]

        # We check if the saved cost is still infinity.
        if saved_cost == float('inf'):
            # If it is infinity, it means this item was missing from the input entirely, so we fail.
            return -1

        # If it wasn't infinity, we add this item's minimum cost to our running total.
        total_cost += saved_cost

    # After adding up the cheapest costs for all items, we return the final sum.
    return total_cost


def run_tests():
    test_cases = [
        {
            "name": "Sample Case 0 (From Image)",
            "numItems": 2,
            "itemId": [0, 1, 0, 1, 1],
            "cost": [4, 74, 47, 744, 7],
            "expected": 11
        },
        {
            "name": "Sample Case 1 (From Image - Missing Item)",
            "numItems": 2,
            "itemId": [1, 1],
            "cost": [4, 7],
            "expected": -1
        },
        {
            "name": "Example Case (From Text)",
            "numItems": 3,
            "itemId": [2, 0, 1, 2],
            "cost": [8, 7, 6, 9],
            "expected": 21
        },
        {
            "name": "Large Data Input Case",
            "numItems": 100000,
            # Generate 100,000 items labeled 0 to 99999
            "itemId": list(range(100000)),
            # Every item costs exactly 2
            "cost": [2] * 100000,
            # 100,000 items * cost of 2 = 200,000
            "expected": 200000
        }
    ]

    print("--- Starting Tests ---")
    for tc in test_cases:
        result = minTotalCost(tc["numItems"], tc["itemId"], tc["cost"])

        if result == tc["expected"]:
            print(f"[PASS] {tc['name']}")
        else:
            print(f"[FAIL] {tc['name']} -> Expected: {tc['expected']}, Got: {result}")
    print("--- Testing Complete ---")


if __name__ == '__main__':
    run_tests()