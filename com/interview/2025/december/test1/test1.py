def find_max_length_equal_zeros_ones(nums):
    """
    Find maximum length subarray with equal 0s and 1s.

    Core Logic:
    - Treat 0 as -1 and 1 as +1
    - Use prefix sum to track running total
    - Same prefix sum at two indices means balanced subarray between them

    Args:
        nums: List of integers containing only 0s and 1s

    Returns:
        Integer representing maximum length of balanced subarray
    """

    # This variable keeps track of our running sum
    # We start at 0 because we haven't seen any elements yet
    prefix_sum = 0

    # This dictionary stores the FIRST occurrence of each prefix sum
    # Key = prefix sum value, Value = index where it first appeared
    # Why store first occurrence? Because we want MAXIMUM length
    # Example: If sum=2 appears at index 3 and index 7
    #          We want index 3 (first) to maximize length (7-3=4)
    first_occurrence = {}

    # IMPORTANT: We initialize with {0: -1}
    # Why? If prefix_sum becomes 0 at index i, it means
    # subarray from index 0 to i is balanced
    # Length would be: i - (-1) = i + 1 (which is correct!)
    first_occurrence[0] = -1

    # This variable stores our answer - the maximum length found so far
    # We start with 0 because minimum possible answer is 0 (no valid subarray)
    max_length = 0

    # Loop through each element in the array
    # 'index' tells us position (0, 1, 2, ...)
    # 'num' is the actual value at that position (0 or 1)
    for index in range(len(nums)):

        # Get current number from array
        num = nums[index]

        # Update running sum based on current number
        # If num is 1: add +1 (sum increases)
        # If num is 0: add -1 (sum decreases)
        # This is the TRICK that makes our algorithm work!
        if num == 1:
            # We saw a 1, so running sum goes up by 1
            prefix_sum = prefix_sum + 1
        else:
            # We saw a 0, so running sum goes down by 1
            # This makes 0 contribute -1 to our sum
            prefix_sum = prefix_sum - 1

        # Now check: have we seen this prefix_sum before?
        if prefix_sum in first_occurrence:
            # YES! We've seen this sum before
            # This means: elements between previous index and current index
            #             sum to zero (equal +1s and -1s, i.e., equal 1s and 0s)

            # Calculate length of this balanced subarray
            # current index minus previous index where same sum occurred
            previous_index = first_occurrence[prefix_sum]
            current_length = index - previous_index

            # Update max_length if this subarray is longer
            # We only keep track of the longest one
            if current_length > max_length:
                max_length = current_length

            # NOTE: We do NOT update first_occurrence here
            # We want to keep the FIRST occurrence to maximize length
        else:
            # NO! This is the first time we see this prefix_sum
            # Store this index as the first occurrence
            first_occurrence[prefix_sum] = index

    # After checking all elements, return the maximum length found
    return max_length


def run_all_tests():
    """
    Main testing function that runs all test cases.
    Prints PASS or FAIL for each test case.
    """

    # Define all test cases as a list of tuples
    # Each tuple contains: (input_array, expected_output, test_description)
    test_cases = [
        # Basic test cases from problem statement
        ([0, 1], 2, "Basic case: single 0 and single 1"),
        ([0, 1, 1, 1, 1, 1, 0, 0, 0], 6, "Example from problem"),

        # Edge cases
        ([], 0, "Empty array"),
        ([0], 0, "Single element 0"),
        ([1], 0, "Single element 1"),
        ([0, 0], 0, "Two zeros - no balanced subarray"),
        ([1, 1], 0, "Two ones - no balanced subarray"),

        # Simple balanced cases
        ([1, 0], 2, "Simple balanced: 1 then 0"),
        ([0, 0, 1, 1], 4, "All balanced"),
        ([1, 1, 0, 0], 4, "All balanced reversed"),

        # Complex cases
        ([0, 1, 0], 2, "Odd length array"),
        ([0, 0, 1, 0, 0, 0, 1, 1], 6, "Complex case"),
        ([1, 1, 1, 1, 0, 0, 0, 0], 8, "Full array balanced"),
        ([0, 1, 1, 0, 1, 1, 1, 0], 4, "Middle balanced section"),

        # Cases where answer is at different positions
        ([1, 0, 1, 1, 1, 0, 0], 6, "Balanced at end"),
        ([0, 0, 1, 0, 1, 1], 6, "Full array balanced"),

        # Alternating pattern
        ([0, 1, 0, 1, 0, 1], 6, "Alternating pattern"),
        ([1, 0, 1, 0, 1, 0], 6, "Alternating pattern reversed"),
    ]

    # Counter for passed tests
    passed_count = 0
    total_count = len(test_cases)

    print("=" * 70)
    print("RUNNING TEST CASES")
    print("=" * 70)

    # Run each test case
    for test_number, (input_array, expected, description) in enumerate(test_cases, 1):

        # Call our solution function
        actual_result = find_max_length_equal_zeros_ones(input_array)

        # Check if result matches expected
        if actual_result == expected:
            status = "PASS ✓"
            passed_count += 1
        else:
            status = "FAIL ✗"

        # Print test result
        print(f"\nTest {test_number}: {status}")
        print(f"  Description: {description}")
        print(f"  Input: {input_array}")
        print(f"  Expected: {expected}")
        print(f"  Actual: {actual_result}")

    print("\n" + "=" * 70)
    print(f"SUMMARY: {passed_count}/{total_count} tests passed")
    print("=" * 70)

    return passed_count == total_count


def run_large_data_tests():
    """
    Test with large inputs to verify performance.
    These tests check if solution handles big data efficiently.
    """

    print("\n" + "=" * 70)
    print("RUNNING LARGE DATA TESTS")
    print("=" * 70)

    import time

    # Test Case 1: Large array with all balanced
    # 500,000 zeros followed by 500,000 ones
    print("\nTest L1: Array of 1,000,000 elements (half 0s, half 1s)")
    large_array_1 = [0] * 500000 + [1] * 500000

    start_time = time.time()
    result_1 = find_max_length_equal_zeros_ones(large_array_1)
    end_time = time.time()

    expected_1 = 1000000  # Entire array is balanced
    status_1 = "PASS ✓" if result_1 == expected_1 else "FAIL ✗"
    print(f"  Result: {result_1}, Expected: {expected_1} - {status_1}")
    print(f"  Time taken: {end_time - start_time:.4f} seconds")

    # Test Case 2: Alternating pattern
    print("\nTest L2: Alternating 0s and 1s (100,000 elements)")
    large_array_2 = [i % 2 for i in range(100000)]

    start_time = time.time()
    result_2 = find_max_length_equal_zeros_ones(large_array_2)
    end_time = time.time()

    expected_2 = 100000  # Full array balanced
    status_2 = "PASS ✓" if result_2 == expected_2 else "FAIL ✗"
    print(f"  Result: {result_2}, Expected: {expected_2} - {status_2}")
    print(f"  Time taken: {end_time - start_time:.4f} seconds")

    # Test Case 3: Random-like pattern (repeating small balanced groups)
    print("\nTest L3: Repeating [0,1,1,0] pattern (400,000 elements)")
    pattern = [0, 1, 1, 0]
    large_array_3 = pattern * 100000

    start_time = time.time()
    result_3 = find_max_length_equal_zeros_ones(large_array_3)
    end_time = time.time()

    expected_3 = 400000  # Full array balanced
    status_3 = "PASS ✓" if result_3 == expected_3 else "FAIL ✗"
    print(f"  Result: {result_3}, Expected: {expected_3} - {status_3}")
    print(f"  Time taken: {end_time - start_time:.4f} seconds")

    # Test Case 4: Unbalanced array (all zeros)
    print("\nTest L4: All zeros (100,000 elements)")
    large_array_4 = [0] * 100000

    start_time = time.time()
    result_4 = find_max_length_equal_zeros_ones(large_array_4)
    end_time = time.time()

    expected_4 = 0  # No balanced subarray possible
    status_4 = "PASS ✓" if result_4 == expected_4 else "FAIL ✗"
    print(f"  Result: {result_4}, Expected: {expected_4} - {status_4}")
    print(f"  Time taken: {end_time - start_time:.4f} seconds")

    print("\n" + "=" * 70)

    all_passed = all([
        result_1 == expected_1,
        result_2 == expected_2,
        result_3 == expected_3,
        result_4 == expected_4
    ])

    return all_passed


# Main execution block
if __name__ == "__main__":
    """
    Entry point of the program.
    Runs all regular tests first, then large data tests.
    """

    print("\n" + "#" * 70)
    print("# MAXIMUM LENGTH SUBARRAY WITH EQUAL 0s AND 1s - TEST SUITE")
    print("#" * 70)

    # Run regular test cases
    regular_tests_passed = run_all_tests()

    # Run large data tests
    large_tests_passed = run_large_data_tests()

    # Final summary
    print("\n" + "#" * 70)
    print("# FINAL RESULT")
    print("#" * 70)

    if regular_tests_passed and large_tests_passed:
        print("\n✓ ALL TESTS PASSED SUCCESSFULLY!")
    else:
        print("\n✗ SOME TESTS FAILED - PLEASE REVIEW")

    print("\n")