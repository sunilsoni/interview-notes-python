def fountainActivation(locations):
    # 'n' stores the total length of the garden, which is equal to the number of fountains.
    n = len(locations)

    # 'max_reach' stores the maximum right boundary reachable from any left starting position (0-indexed).
    # We need this to quickly look up the best fountain to activate from our current spot.
    max_reach = [0] * n

    # We loop through every fountain position, using 'i' from 1 to n (1-based position as per the problem).
    # This loop maps out the coverage bounds for every single fountain in the array.
    for i in range(1, n + 1):
        # 'left_bound' determines how far to the left the current fountain's water reaches.
        # We use max(1, ...) to ensure the water doesn't theoretically extend past the start of the garden.
        left_bound = max(1, i - locations[i - 1])

        # 'right_bound' determines how far to the right the current fountain's water reaches.
        # We use min(n, ...) to ensure the water doesn't theoretically extend past the end of the garden.
        right_bound = min(n, i + locations[i - 1])

        # We update 'max_reach' at the (left_bound - 1) index to store the furthest right_bound found so far.
        # This is vital: if multiple fountains start at the same left point, we only want the one that shoots furthest right.
        max_reach[left_bound - 1] = max(max_reach[left_bound - 1], right_bound)

    # 'fountains_activated' acts as our counter for how many fountains we ultimately turn on.
    # It initializes at 0 before we start evaluating the garden path.
    fountains_activated = 0

    # 'current_covered_end' tracks the furthest right point the currently activated fountains manage to cover.
    # It starts at 0, representing the beginning of the garden before any water is flowing.
    current_covered_end = 0

    # 'next_possible_end' tracks the absolute furthest right point we can reach by turning on just one additional fountain.
    # We will continuously update this value as we scan through the garden's positions.
    next_possible_end = 0

    # We iterate over the garden positions 'i' from 0 to n-1 to simulate walking through the garden.
    # This greedy loop allows us to pick the minimal number of optimal fountains.
    for i in range(n):

        # We update 'next_possible_end' by comparing its current value with the furthest reach of fountains starting at position 'i'.
        # This guarantees we always know the best possible fountain to turn on next.
        next_possible_end = max(next_possible_end, max_reach[i])

        # We check if our walking position 'i' has reached the very edge of our currently covered watered zone.
        # If they match, it means we must absolutely activate a new fountain to prevent dry patches.
        if i == current_covered_end:

            # We increment our counter because the algorithm forces us to turn on a new fountain here.
            fountains_activated += 1

            # We extend our safe watered zone forward to the best 'next_possible_end' we discovered.
            current_covered_end = next_possible_end

            # We check if our newly extended water coverage reaches or surpasses the garden's total length 'n'.
            # This is our termination condition, confirming the entire garden is successfully watered.
            if current_covered_end >= n:
                # We break out of the loop early to save processing time since our goal is completely met.
                break

    # Finally, we return the total count of fountains that were activated.
    # This returns the minimal optimal set required by the problem statement.
    return fountains_activated
def main():
    test_cases = [
        {
            "name": "Sample Case 0",
            "locations": [1, 1, 1],
            "expected": 1
        },
        {
            "name": "Sample Case 1",
            "locations": [2, 0, 0, 0],
            "expected": 2
        },
        {
            "name": "Edge Case: All Zeros (No ranges)",
            "locations": [0, 0, 0, 0, 0],
            "expected": 5 # Each fountain only covers itself
        },
        {
            "name": "Edge Case: First fountain covers everything",
            "locations": [10, 0, 0, 0, 0],
            "expected": 1
        },
        {
            "name": "Large Data: 100,000 Fountains with 0 reach",
            "locations": [0] * 100000,
            "expected": 100000
        },
        {
            "name": "Large Data: 100,000 Fountains, one covers all",
            "locations": [100000] * 100000,
            "expected": 1
        }
    ]

    print("--- Running Tests ---")
    for index, test in enumerate(test_cases):
        result = fountainActivation(test["locations"])
        status = "PASS" if result == test["expected"] else f"FAIL (Got {result}, Expected {test['expected']})"
        print(f"Test {index + 1}: {test['name']} -> {status}")

if __name__ == "__main__":
    main()