import math

import math  # Import math library for mathematical functions (e.g., math.ceil)

def min_delivery_speed(packages, h):
    # Define a helper function to check if all packages can be delivered within h hours at speed k.
    def can_deliver_with_speed(k):
        # Calculate total hours required to deliver all packages given speed k
        total_hours = sum(math.ceil(p / k) for p in packages)
        # Return True if total_hours is less than or equal to available hours h
        return total_hours <= h

    # Initialize binary search bounds: low = 1, high = maximum packages at any location
    low, high = 1, max(packages)
    # Initialize result with the highest possible speed (worst-case scenario)
    result = high

    # Binary search loop: continue while low bound is less than or equal to high bound
    while low <= high:
        mid = (low + high) // 2  # Calculate the mid value of current search bounds
        # Check if mid speed is sufficient to deliver all packages within h hours
        if can_deliver_with_speed(mid):
            result = mid         # Update result to current mid because it's a potential answer
            high = mid - 1       # Search for a smaller valid speed in the lower half
        else:
            low = mid + 1        # If not sufficient, try a larger speed in the upper half

    # After exiting loop, result contains the minimum k that satisfies the condition
    return result


# Testing framework
def run_tests():
    test_cases = [
        # Provided test case
        {"packages": [3, 6, 7, 11], "h": 8, "expected": 4},
        # Edge cases
        {"packages": [1], "h": 1, "expected": 1},                # Single location, h equals packages
        {"packages": [1000000], "h": 1000000, "expected": 1},    # High h, low speed needed
        {"packages": [1000000], "h": 1, "expected": 1000000},    # One location but one hour
        {"packages": [30, 11, 23, 4, 20], "h": 6, "expected": 23},  # Another sample scenario

        # Large data test
        {"packages": [1000000] * 100000, "h": 100000000, "expected": 1},  # Many locations, high h
    ]

    for idx, test in enumerate(test_cases):
        packages = test["packages"]
        h = test["h"]
        expected = test["expected"]
        result = min_delivery_speed(packages, h)
        outcome = "PASS" if result == expected else "FAIL"
        print(f"Test case {idx + 1}: {outcome} (Expected: {expected}, Got: {result})")

if __name__ == "__main__":
    run_tests()
