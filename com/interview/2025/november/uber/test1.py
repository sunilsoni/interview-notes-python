def find_next_palindrome(num):
    """
    Finds the smallest palindrome greater than the given number.
    Uses a constructive approach to build the palindrome efficiently.
    """

    # Convert the input number to string for easier digit manipulation
    # String allows us to access individual digits and compare easily
    num_str = str(num)

    # Store the length of the number for later calculations
    # We'll use this to find middle digits and construct new palindromes
    length = len(num_str)

    # Special Case: Check if all digits are 9 (like 99, 999, 9999)
    # These always result in 10...01 pattern (99→101, 999→1001)
    if all(digit == '9' for digit in num_str):
        # Return 1 followed by (length-1) zeros and ending with 1
        # Example: 999 has length 3, so we return 1001
        return int('1' + '0' * (length - 1) + '1')

    # Main approach: Try to create palindrome by mirroring
    # First, let's try simply mirroring the left half to the right

    # Calculate the middle index to split the number
    # For odd length: middle is the center digit
    # For even length: middle is where we split the halves
    is_odd = length % 2 == 1  # Check if length is odd
    mid = length // 2  # Integer division to find middle position

    # Extract the left half of the number
    # For odd length numbers, we exclude the middle digit initially
    left_half = num_str[:mid]

    # Create a palindrome by mirroring the left half
    # For odd length: left + middle + reversed(left)
    # For even length: left + reversed(left)
    if is_odd:
        # Include the middle digit for odd-length numbers
        middle_digit = num_str[mid]
        # Create palindrome: left half + middle + reversed left half
        palindrome = left_half + middle_digit + left_half[::-1]
    else:
        # For even length, just mirror the left half
        palindrome = left_half + left_half[::-1]

    # Check if this palindrome is greater than our input
    # If yes, we found our answer!
    if int(palindrome) > num:
        return int(palindrome)

    # If mirroring didn't work, we need to increment and then mirror
    # This happens when the right half is already larger than mirrored left

    # We'll increment the "middle part" of the number
    if is_odd:
        # For odd length, increment the middle digit
        middle_digit = str(int(num_str[mid]) + 1)

        # Check if middle digit became 10 (was 9, now needs carry)
        if middle_digit == '10':
            # Need to handle carry-over to left half
            # Convert left half to integer, add 1, then back to string
            left_half_int = int(left_half) if left_half else 0
            left_half = str(left_half_int + 1)
            middle_digit = '0'  # Reset middle digit after carry

            # Check if carry caused overflow (all were 9s in left+middle)
            # This would make our number longer
            if len(left_half) > mid:
                # Number grew in length, return 10...01 pattern
                return int('1' + '0' * (length - 1) + '1')

        # Construct the new palindrome with incremented middle
        palindrome = left_half + middle_digit + left_half[::-1]
    else:
        # For even length, increment the left half
        left_half_int = int(left_half)
        left_half = str(left_half_int + 1)

        # Check if incrementing caused overflow (left half was all 9s)
        if len(left_half) > mid:
            # Number grew in length, return 10...01 pattern
            return int('1' + '0' * (length - 1) + '1')

        # Create palindrome with incremented left half
        palindrome = left_half + left_half[::-1]

    # Return the final palindrome as an integer
    return int(palindrome)


def main():
    """
    Test method to validate the palindrome function with various test cases.
    Includes edge cases and large number handling.
    """

    # Define test cases as tuples of (input, expected_output)
    # Each tuple represents one test scenario
    test_cases = [
        # Basic test cases from problem statement
        (1000, 1001),  # Simple case
        (1200, 1221),  # Another basic case

        # Edge cases with single digit numbers
        (0, 1),  # Smallest input
        (8, 9),  # Single digit to single digit
        (9, 11),  # 9 is special, next palindrome is 11

        # Cases with all 9s (special handling required)
        (99, 101),  # Two 9s
        (999, 1001),  # Three 9s
        (9999, 10001),  # Four 9s

        # Palindromes as input (need next palindrome)
        (121, 131),  # Input is already palindrome
        (1221, 1331),  # Even length palindrome input

        # Random cases to test logic
        (1991, 2002),  # Crosses into next thousand
        (12321, 12421),  # Five digit palindrome
        (123456, 124421),  # Six digit number

        # Large number test cases (performance check)
        (99999999, 100000001),  # Eight 9s
        (123456789, 123464321),  # Large random number
        (999999999, 1000000001),  # Nine 9s - billion range
    ]

    # Counter variables to track test results
    passed_tests = 0  # Count of successful tests
    failed_tests = 0  # Count of failed tests

    # Print header for test results
    print("=" * 60)
    print("PALINDROME FINDER - TEST RESULTS")
    print("=" * 60)

    # Iterate through each test case
    for i, (input_num, expected) in enumerate(test_cases, 1):
        # Try to find the next palindrome for current input
        try:
            # Call our function with the test input
            result = find_next_palindrome(input_num)

            # Check if result matches expected output
            if result == expected:
                # Test passed - increment counter and show success
                passed_tests += 1
                status = "✓ PASS"
                print(f"Test {i:2d}: {status} | Input: {input_num:10d} | "
                      f"Output: {result:10d} | Expected: {expected:10d}")
            else:
                # Test failed - increment counter and show failure
                failed_tests += 1
                status = "✗ FAIL"
                print(f"Test {i:2d}: {status} | Input: {input_num:10d} | "
                      f"Output: {result:10d} | Expected: {expected:10d}")

        except Exception as e:
            # Handle any unexpected errors during execution
            failed_tests += 1
            print(f"Test {i:2d}: ✗ ERROR | Input: {input_num} | Error: {str(e)}")

    # Print summary of test results
    print("=" * 60)
    print(f"SUMMARY: {passed_tests} PASSED | {failed_tests} FAILED | "
          f"Total: {len(test_cases)}")
    print("=" * 60)

    # Additional test for extremely large numbers (stress test)
    print("\nSTRESS TEST - Very Large Numbers:")
    print("-" * 60)

    # Test with a massive number to verify performance
    large_input = 12345678901234567890
    print(f"Input: {large_input}")

    # Measure time taken for large number
    import time
    start_time = time.time()
    large_result = find_next_palindrome(large_input)
    end_time = time.time()

    print(f"Output: {large_result}")
    print(f"Time taken: {end_time - start_time:.6f} seconds")

    # Verify the result is indeed a palindrome
    result_str = str(large_result)
    is_palindrome = result_str == result_str[::-1]
    print(f"Is palindrome: {is_palindrome}")
    print(f"Is greater than input: {large_result > large_input}")


# Entry point of the program
if __name__ == "__main__":
    # Execute the main test function when script is run directly
    main()