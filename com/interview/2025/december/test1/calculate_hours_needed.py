import math  # We need ceil function for rounding up


def calculate_hours_needed(items, speed):
    """
    Calculate total hours needed to rob all houses at given speed.

    For each house:
    - If items <= speed: takes 1 hour (finish and chill)
    - If items > speed: takes ceil(items/speed) hours

    Args:
        items: List of items in each house
        speed: Stealing speed (items per hour)

    Returns:
        Total hours needed to rob all houses
    """

    # Start with zero hours
    total_hours = 0

    # Go through each house one by one
    for item_count in items:
        # Calculate hours needed for this house
        # ceil(a/b) rounds up - because partial hour = full hour
        # Example: 7 items at speed 4 = ceil(7/4) = ceil(1.75) = 2 hours
        hours_for_this_house = math.ceil(item_count / speed)

        # Add to total
        total_hours = total_hours + hours_for_this_house

    # Return total hours for all houses
    return total_hours


def find_minimum_speed(items, h):
    """
    Find minimum stealing speed to rob all houses within h hours.

    Uses binary search to efficiently find the answer.

    Args:
        items: List of items in each house
        h: Hours available before sunrise

    Returns:
        Minimum speed needed
    """

    # Edge case: empty array
    # If no houses, no speed needed
    if len(items) == 0:
        return 0

    # Set up binary search range
    # Minimum possible speed is 1 (steal at least 1 item per hour)
    low = 1

    # Maximum possible speed is the largest house
    # At this speed, every house takes exactly 1 hour
    high = max(items)

    # Store the answer as we search
    # Start with max speed (we know this works for sure)
    answer = high

    # Binary search loop
    # Continue while search range is valid
    while low <= high:

        # Find middle speed to test
        # This is our candidate speed
        mid = (low + high) // 2

        # Calculate how many hours needed at this speed
        hours_needed = calculate_hours_needed(items, mid)

        # Check if this speed is fast enough
        if hours_needed <= h:
            # YES! This speed works
            # Save it as potential answer
            answer = mid

            # But maybe we can go slower?
            # Search in lower half for smaller speed
            high = mid - 1
        else:
            # NO! This speed is too slow
            # Need faster speed
            # Search in upper half
            low = mid + 1

    # Return the minimum speed found
    return answer


def run_all_tests():
    """
    Test function to verify our solution.
    Runs multiple test cases and reports PASS/FAIL.
    """

    # Define test cases: (items, hours, expected_output, description)
    test_cases = [
        # Given examples
        ([3, 6, 7, 11], 8, 4, "Example 1 from problem"),
        ([30, 11, 23, 4, 20], 5, 30, "Example 2 - minimum hours"),
        ([30, 11, 23, 4, 20], 6, 23, "Example 3 - one extra hour"),

        # Edge cases
        ([1], 1, 1, "Single house single hour"),
        ([10], 1, 10, "Single house must finish in 1 hour"),
        ([10], 10, 1, "Single house with plenty of time"),
        ([1, 1, 1, 1], 4, 1, "All houses have 1 item"),

        # More complex cases
        ([2, 2], 2, 2, "Two houses two hours"),
        ([2, 2], 3, 1, "Two houses three hours"),
        ([5, 5, 5, 5], 4, 5, "Equal items minimum hours"),
        ([5, 5, 5, 5], 8, 3, "Equal items double hours"),
        ([1, 2, 3, 4, 5], 5, 5, "Increasing items minimum hours"),
        ([1, 2, 3, 4, 5], 10, 2, "Increasing items more hours"),

        # Large values
        ([100, 200, 300], 3, 300, "Large items minimum hours"),
        ([100, 200, 300], 6, 100, "Large items double hours"),
    ]

    # Track results
    passed = 0
    total = len(test_cases)

    print("=" * 60)
    print("RUNNING TEST CASES")
    print("=" * 60)

    # Run each test
    for i, (items, h, expected, desc) in enumerate(test_cases, 1):

        # Get actual result
        actual = find_minimum_speed(items, h)

        # Check if correct
        if actual == expected:
            status = "PASS ✓"
            passed += 1
        else:
            status = "FAIL ✗"

        # Print result
        print(f"\nTest {i}: {status}")
        print(f"  Description: {desc}")
        print(f"  Input: items={items}, h={h}")
        print(f"  Expected: {expected}, Actual: {actual}")

    # Summary
    print("\n" + "=" * 60)
    print(f"SUMMARY: {passed}/{total} tests passed")
    print("=" * 60)

    return passed == total


def run_large_data_tests():
    """
    Test with large inputs for performance verification.
    """

    import time

    print("\n" + "=" * 60)
    print("LARGE DATA TESTS")
    print("=" * 60)

    # Test 1: Many houses
    print("\nTest L1: 100,000 houses")
    large_items_1 = [i % 1000 + 1 for i in range(100000)]
    h1 = 100000

    start = time.time()
    result1 = find_minimum_speed(large_items_1, h1)
    end = time.time()

    print(f"  Result: {result1}")
    print(f"  Time: {end - start:.4f} seconds")

    # Test 2: Large item counts
    print("\nTest L2: Houses with up to 1,000,000 items")
    large_items_2 = [1000000, 500000, 750000, 250000]
    h2 = 4

    start = time.time()
    result2 = find_minimum_speed(large_items_2, h2)
    end = time.time()

    expected2 = 1000000  # Must finish each in 1 hour
    status2 = "PASS ✓" if result2 == expected2 else "FAIL ✗"

    print(f"  Result: {result2}, Expected: {expected2} - {status2}")
    print(f"  Time: {end - start:.4f} seconds")

    # Test 3: Many houses with large items
    print("\nTest L3: 50,000 houses with large items")
    large_items_3 = [100000] * 50000
    h3 = 100000

    start = time.time()
    result3 = find_minimum_speed(large_items_3, h3)
    end = time.time()

    expected3 = 50000  # 100000/50000 = 2 hours each = 100000 total
    status3 = "PASS ✓" if result3 == expected3 else "FAIL ✗"

    print(f"  Result: {result3}, Expected: {expected3} - {status3}")
    print(f"  Time: {end - start:.4f} seconds")

    print("\n" + "=" * 60)


# Main execution
if __name__ == "__main__":

    print("\n" + "#" * 60)
    print("# ROBBER MINIMUM SPEED PROBLEM - TEST SUITE")
    print("#" * 60)

    # Run all tests
    all_passed = run_all_tests()

    # Run large data tests
    run_large_data_tests()

    # Final result
    print("\n" + "#" * 60)
    if all_passed:
        print("# ALL TESTS PASSED! ✓")
    else:
        print("# SOME TESTS FAILED ✗")
    print("#" * 60)


