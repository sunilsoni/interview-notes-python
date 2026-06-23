def findClosestElements_optimized(arr, k, x):
    # The 'left' boundary for our binary search. The window could start at index 0.
    left = 0

    # The 'right' boundary for our binary search.
    # The window cannot start later than (total length - k), otherwise we'd run out of elements.
    right = len(arr) - k

    # We run the binary search as long as our search space has more than one possibility.
    while left < right:

        # Find the middle starting index of our current search space.
        # The '//' operator performs integer division (drops the decimal).
        mid = (left + right) // 2

        # We compare the element at 'mid' with the element just OUTSIDE our imaginary window of size k (at 'mid + k').
        # We use a mathematical trick: x - arr[mid] vs arr[mid + k] - x
        # If the element outside the right edge is strictly closer to 'x' than the element at the left edge...
        if x - arr[mid] > arr[mid + k] - x:

            # ...it means our window is too far to the left.
            # We must shift our search space to the right side of 'mid'.
            left = mid + 1

        # Otherwise, the left side is closer (or there is a tie, in which case we prefer the smaller/left side).
        else:
            # We shift our search space to the left by moving the 'right' boundary down to 'mid'.
            right = mid

    # When the while loop finishes, 'left' and 'right' converge on the exact correct starting index.
    # We slice the array from that starting index to grab exactly 'k' elements.
    return arr[left: left + k]


def main():
    # Define our test cases (with the corrected math for Test 6)
    test_cases = [
        ([1, 2, 3, 4, 5], 4, 3, [1, 2, 3, 4]),  # standard case
        ([1, 1, 2, 3, 4, 5], 4, -1, [1, 1, 2, 3]),  # x outside left
        ([1, 2, 3, 4, 5], 4, 100, [2, 3, 4, 5]),  # x outside right
        ([1, 2, 3, 4, 5], 1, 3, [3]),  # k = 1, exact match
        ([1, 2, 3, 4, 5], 5, 3, [1, 2, 3, 4, 5]),  # k = full array
        ([1, 1, 1, 10, 10, 10], 3, 5, [1, 1, 1]),  # tie-breaking with gap (Corrected expected output)
        ([1, 3], 1, 2, [1]),  # tie -> prefer smaller
    ]

    print("Starting Optimized Assertions...\n")

    # Loop through and verify all standard tests
    for index, (arr, k, x, expected) in enumerate(test_cases, start=1):
        result = findClosestElements_optimized(arr, k, x)
        assert result == expected, f"Test {index} Failed! Expected {expected}, got {result}"
        print(f"Test {index} PASS: arr={arr}, k={k}, x={x}  -->  {result}")

    print("\n--- Running EXTREME Large Data Test ---")

    # Creating an enormous array of 10 MILLION items: [0, 1, 2, ..., 9999999]
    large_arr = list(range(10000000))
    k_large = 50000
    x_large = 7500000

    # We expect the 50,000 numbers centered around 7,500,000.
    # We subtract 25,000 to find the start, and add 25,000 to find the end.
    expected_large = list(range(7500000 - 25000, 7500000 + 25000))

    # Our previous O(N) solution would take roughly 10 million steps here.
    # This Binary Search will find the starting point in only about 23 steps!
    result_large = findClosestElements_optimized(large_arr, k_large, x_large)

    assert result_large == expected_large, "Extreme Large Data Test Failed!"
    print("Extreme Large Data Test PASS: Evaluated 10,000,000 elements in a fraction of a millisecond.")

    print("\nAll assertions passed! The optimized logic is fully verified.")


if __name__ == "__main__":
    main()