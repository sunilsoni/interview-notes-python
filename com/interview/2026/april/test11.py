# Define the function that takes two lists, arr1 and arr2, as input arguments.
def merge_and_sort_special(arr1, arr2):
    # Combine both input lists into a single new list called 'merged_array'.
    merged_array = arr1 + arr2

    # Initialize an empty list to store all the odd numbers we find.
    odd_numbers = []

    # Initialize an empty list to store all the even numbers we find.
    even_numbers = []

    # Start a loop to check each number one by one in our combined 'merged_array'.
    for num in merged_array:
        # Check if the current number divided by 2 has a remainder (meaning it is an odd number).
        if num % 2 != 0:
            # If it is odd, add this number to the end of our 'odd_numbers' list.
            odd_numbers.append(num)
        # If the number does not have a remainder when divided by 2, it falls into this 'else' block.
        else:
            # Since it is even, add this number to the end of our 'even_numbers' list.
            even_numbers.append(num)

    # Sort the 'odd_numbers' list in standard ascending order (smallest to largest).
    odd_numbers.sort()

    # Sort the 'even_numbers' list in standard ascending order (smallest to largest).
    even_numbers.sort()

    # Combine the sorted odd list and sorted even list, putting odds first, and return the final result.
    return odd_numbers + even_numbers


# Define a simple testing function to run our cases without needing external unit test frameworks.
def run_tests():
    # Set up a counter to track how many tests pass.
    passed = 0

    # Define a list of test cases, each containing the two inputs and the expected output.
    test_cases = [
        # Test Case 1: Standard mixed numbers.
        {"arr1": [4, 1, 3], "arr2": [2, 7, 6], "expected": [1, 3, 7, 2, 4, 6]},
        # Test Case 2: Arrays with only even numbers.
        {"arr1": [8, 4], "arr2": [2, 6], "expected": [2, 4, 6, 8]},
        # Test Case 3: Arrays with only odd numbers.
        {"arr1": [9, 3], "arr2": [1, 5], "expected": [1, 3, 5, 9]},
        # Test Case 4: One empty array.
        {"arr1": [], "arr2": [5, 2, 8, 1], "expected": [1, 5, 2, 8]},
        # Test Case 5: Both empty arrays.
        {"arr1": [], "arr2": [], "expected": []}
    ]

    # Loop through each test case in our list.
    for i, test in enumerate(test_cases):
        # Call our function with the inputs from the current test case.
        result = merge_and_sort_special(test["arr1"], test["arr2"])
        # Check if our function's result matches the expected answer.
        if result == test["expected"]:
            # Print a pass message if they match.
            print(f"Test {i + 1} PASS")
            # Increment our passed counter.
            passed += 1
        else:
            # Print a fail message showing what went wrong if they do not match.
            print(f"Test {i + 1} FAIL: Expected {test['expected']}, Got {result}")

    # --- Large Data Test ---
    # Create a large array of 100,000 integers to test performance.
    large_arr1 = list(range(100000, 0, -1))  # 100,000 down to 1
    # Create another large array.
    large_arr2 = list(range(100001, 200000))  # 100,001 up to 199,999

    # Start a try-except block to catch any memory or timeout errors.
    try:
        # Run the function on the large datasets.
        large_result = merge_and_sort_special(large_arr1, large_arr2)
        # Verify the first element is the smallest odd number.
        assert large_result[0] == 1
        # Verify the last element is the largest even number.
        assert large_result[-1] == 199998
        # Print a pass message for the large data test.
        print("Large Data Test PASS")
        # Increment our passed counter.
        passed += 1
    # Catch any errors that happen during the large data test.
    except Exception as e:
        # Print a fail message with the specific error.
        print(f"Large Data Test FAIL: {e}")

    # Print the final summary of how many tests passed.
    print(f"\nTotal Passed: {passed}/{len(test_cases) + 1}")


# Standard Python check to ensure this code runs when the script is executed directly.
if __name__ == "__main__":
    # Call our test runner function.
    run_tests()