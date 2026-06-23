def findClosestElements(arr, k, x):
    # Place the left pointer at the very beginning of the array (index 0).
    left = 0

    # Place the right pointer at the very end of the array.
    # The last index is the total length of the array minus 1.
    right = len(arr) - 1

    # Loop to shrink our window until exactly 'k' elements are left.
    # (right - left) gives us the number of elements in our window minus 1.
    while (right - left) >= k:

        # Calculate the absolute distance between the leftmost element and target 'x'.
        dist_left = abs(arr[left] - x)

        # Calculate the absolute distance between the rightmost element and target 'x'.
        dist_right = abs(arr[right] - x)

        # Check if the element on the left is further away from 'x' than the element on the right.
        if dist_left > dist_right:
            # If the left element is further, move the pointer one step to the right (shrink from left).
            left += 1

        # If the right element is further away, OR if both distances are exactly the same (a tie)...
        else:
            # ...remove the right element because the rules say the smaller element wins a tie.
            # Move the pointer one step to the left (shrink from right).
            right -= 1

    # Return the 'k' elements that are left inside our pointers using slicing.
    return arr[left: left + k]


def main():
    # Define the test cases exactly as provided in the screenshot
    test_cases = [
        # (arr, k, x, expected)
        ([1, 2, 3, 4, 5], 4, 3, [1, 2, 3, 4]),  # standard case
        ([1, 1, 2, 3, 4, 5], 4, -1, [1, 1, 2, 3]),  # x outside left
        ([1, 2, 3, 4, 5], 4, 100, [2, 3, 4, 5]),  # x outside right
        ([1, 2, 3, 4, 5], 1, 3, [3]),  # k = 1, exact match
        ([1, 2, 3, 4, 5], 5, 3, [1, 2, 3, 4, 5]),  # k = full array
        ([1, 1, 1, 10, 10, 10], 3, 5, [1, 1, 10]),  # tie-breaking with gap
        ([1, 3], 1, 2, [1]),  # tie -> prefer smaller
    ]

    print("Starting Assertions...\n")

    # Loop through each test case. Using enumerate to number them starting from 1.
    for index, (arr, k, x, expected) in enumerate(test_cases, start=1):
        # Call our function to get the actual computed result
        result = findClosestElements(arr, k, x)

        # Use assert to check if result matches expected.
        # If it doesn't, it immediately crashes and prints the error message provided.
        assert result == expected, f"Test {index} Failed! Expected {expected}, got {result}"

        # If the code reaches this line, the assert passed successfully.
        print(f"Test {index} PASS: arr={arr}, k={k}, x={x}  -->  {result}")

    print("\n--- Running Large Data Test ---")
    # Creating a large array of 10,000 items: [0, 1, 2, ..., 9999]
    large_arr = list(range(10000))
    k_large = 5000
    x_large = 2500
    # Expected: The 5000 numbers closest to 2500 will be from 0 to 4999.
    expected_large = list(range(0, 5000))

    # Asserting the large dataset
    assert findClosestElements(large_arr, k_large, x_large) == expected_large, "Large Data Test Failed!"
    print("Large Data Test PASS: Evaluated 10,000 elements instantly.")

    # Final confirmation message
    print("\nAll assertions passed! The logic is fully verified.")


# Execute the main testing block
if __name__ == "__main__":
    main()