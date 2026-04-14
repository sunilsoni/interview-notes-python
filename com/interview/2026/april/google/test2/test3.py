import time  # We import the time module to measure how fast our tests run
from collections import deque  # We import deque to efficiently manage our sliding window elements


def max_sliding_window(nums, k):  # Define the function taking the list of numbers and the window size
    # First, handle edge cases: if the array is empty, window size is 0, or k is invalid
    if not nums or k == 0:  # Check if the input list is empty or if the window size is zero
        return []  # If invalid, return an empty list immediately because there are no windows

    result = []  # Initialize an empty list to store the maximum values for each window
    window = deque()  # Initialize an empty double-ended queue to store the *indices* of elements

    for i in range(len(nums)):  # Loop through the array using 'i' as the current index

        # Step 1: Clean up the front of the deque (remove elements outside the current window)
        # We check if the deque has items AND if the index at the front is too old (out of bounds)
        while window and window[0] < i - k + 1:  # The left bound of the window is 'i - k + 1'
            window.popleft()  # Remove the oldest index from the front because it is no longer in the window

        # Step 2: Clean up the back of the deque (remove smaller elements)
        # We check if the current number is bigger than the numbers represented by indices at the back
        while window and nums[window[-1]] < nums[i]:  # If the new number is larger, older smaller ones are useless
            window.pop()  # Remove the smaller number's index from the back of the deque

        # Step 3: Add the current element's index to the deque
        window.append(i)  # Add the current index 'i' to the back of our deque for future comparisons

        # Step 4: Record the maximum value if our window has reached the required size 'k'
        # We only start recording when our current index 'i' has moved at least 'k - 1' steps
        if i >= k - 1:  # Check if we have processed enough elements to form our first full window
            result.append(nums[window[0]])  # The front of the deque always holds the index of the max value

    return result  # Finally, return the list of maximums


# ---------------------------------------------------------
# Testing Section (Custom Test Runner without Unittest)
# ---------------------------------------------------------

def run_test(test_name, nums, k, expected):  # Define a helper function to run and validate tests
    start_time = time.time()  # Start a timer to track performance
    actual = max_sliding_window(nums, k)  # Call our main logic function to get the actual result
    end_time = time.time()  # Stop the timer once the function finishes

    time_taken_ms = (end_time - start_time) * 1000  # Convert the time taken into milliseconds

    if actual == expected:  # Check if the output matches what we expected
        print(f"PASS: {test_name} (Time: {time_taken_ms:.2f} ms)")  # Print a success message with the time
    else:  # If the output doesn't match
        print(f"FAIL: {test_name}")  # Print a failure message
        print(f"  Expected: {expected[:10]}...")  # Print a snippet of what we expected (truncated for safety)
        print(f"  Actual:   {actual[:10]}...")  # Print a snippet of what we actually got


def main():  # Define the main execution block
    # Test Case 1: The exact example provided in the typical problem description
    run_test(
        test_name="Standard Example Test",
        nums=[1, 3, -1, -3, 5, 3, 6, 7],
        k=4,
        expected=[3, 5, 5, 6, 7]
    )

    # Test Case 2: Window size is 1 (the max is just every single element itself)
    run_test(
        test_name="Window Size 1",
        nums=[9, 8, 7, 6],
        k=1,
        expected=[9, 8, 7, 6]
    )

    # Test Case 3: A strictly increasing array (max is always the newest element)
    run_test(
        test_name="Increasing Array",
        nums=[1, 2, 3, 4, 5],
        k=2,
        expected=[2, 3, 4, 5]
    )

    # Test Case 4: Large Data Input Test to ensure our logic doesn't crash or take too long
    large_size = 100000  # Define a massive size for the array (100k elements)
    large_nums = list(range(large_size))  # Generate a list from 0 to 99,999
    # If k=3, the maxes for an increasing array will just be the elements starting from index 2
    large_expected = list(range(2, large_size))

    run_test(
        test_name="Large Data Test (100k elements)",
        nums=large_nums,
        k=3,
        expected=large_expected
    )


# Execute the main function if this script is run directly
if __name__ == "__main__":
    main()