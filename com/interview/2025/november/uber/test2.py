# We implement everything in plain Python 3.


def next_palindrome_greater_than(num: int) -> int:
    """
    Given an integer num, return the smallest palindrome strictly greater than num.
    """

    # We first move to the next integer after 'num' because
    # the problem wants a palindrome strictly greater than 'num'.
    # Example: if num = 1000, we start from 1001.
    start_value = num + 1

    # Convert this integer to a string so that it is easy
    # to work with individual digits.
    start_str = str(start_value)

    # Turn the string into a list of characters (digits).
    # Using a list is helpful because lists are mutable,
    # so we can change digits in place.
    digits = list(start_str)

    # Keep a copy of the numeric value as an integer.
    # This is equal to start_value, but we store it here
    # to make the comparison step very clear.
    original_numeric = int(start_str)

    # -------------------------------------------------------------------------
    # Helper function: mirror_from_left
    # -------------------------------------------------------------------------
    # This function takes a list of digit characters and mirrors the left side
    # onto the right side to form a palindrome.
    # Example:
    #   Input digits: ['1', '2', '9', '0']
    #   After mirroring: ['1', '2', '2', '1']  (which is 1221)
    # We modify the list in place and do not return anything.
    # -------------------------------------------------------------------------
    def mirror_from_left(digit_list: list) -> None:
        # 'left' will move from the beginning toward the center.
        left = 0
        # 'right' will move from the end toward the center.
        right = len(digit_list) - 1

        # We loop while 'left' index is strictly less than 'right' index.
        # Each step, we copy the digit at 'left' to the position 'right'.
        while left < right:
            # Copy the left digit onto the right side
            # so that the number becomes symmetric.
            digit_list[right] = digit_list[left]

            # Move 'left' one step to the right.
            left += 1

            # Move 'right' one step to the left.
            right -= 1
        # When the loop ends, the list represents a palindrome.

    # -------------------------------------------------------------------------
    # Step 1: Create an initial palindrome by mirroring from left.
    # -------------------------------------------------------------------------

    # Make a separate copy of the digits list so that we can modify it
    # without changing the original digits directly.
    palindrome_digits = digits[:]

    # Mirror the left side of the digits onto the right side to form
    # an initial palindrome candidate.
    mirror_from_left(palindrome_digits)

    # Turn the list of digits back into a string representation.
    palindrome_str = "".join(palindrome_digits)

    # Convert that string to an integer so we can compare numeric values.
    palindrome_value = int(palindrome_str)

    # -------------------------------------------------------------------------
    # Step 2: Check if this palindrome is already >= original_numeric.
    # -------------------------------------------------------------------------

    # If our mirrored palindrome is already greater than or equal to the
    # starting numeric value, we are done.
    # It is guaranteed to be strictly greater than the original 'num'
    # because we started from 'num + 1'.
    if palindrome_value >= original_numeric:
        # Return the palindrome as the final answer.
        return palindrome_value

    # -------------------------------------------------------------------------
    # Step 3: If the mirrored palindrome is too small, we need a bigger one.
    #         We do this by incrementing the middle digit(s) and then mirroring again.
    # -------------------------------------------------------------------------

    # We start with a carry of 1 because we want to add 1 to the "middle" area.
    carry = 1

    # 'length' holds the current number of digits.
    length = len(palindrome_digits)

    # We compute the index from which to start incrementing.
    # For an odd length, this is exactly the middle index.
    # For an even length, this will be the left of the two center positions.
    # Example:
    #   length = 4 -> center index = (4 - 1) // 2 = 1 (second digit)
    #   length = 5 -> center index = (5 - 1) // 2 = 2 (third digit)
    center_index = (length - 1) // 2

    # We now move from this center index to the left,
    # applying the carry as we go.
    index = center_index

    # We keep looping while we still have a carry to apply
    # and the index is still within the list (>= 0).
    while index >= 0 and carry > 0:
        # Convert the digit character at the current index to an integer
        # so we can do arithmetic on it.
        current_digit = int(palindrome_digits[index])

        # Add the carry to this digit.
        new_digit_value = current_digit + carry

        # The new digit after addition is the remainder of division by 10.
        # Example: if current_digit = 9 and carry = 1,
        # new_digit_value = 10 -> new digit becomes 0.
        palindrome_digits[index] = str(new_digit_value % 10)

        # The new carry is the division result by 10.
        # Example: if new_digit_value = 10, then carry becomes 1.
        carry = new_digit_value // 10

        # Move to the previous digit on the left side for the next iteration.
        index -= 1

    # After the loop ends, if 'carry' is still 1,
    # it means we have overflowed beyond the most significant digit.
    # Example: 999 -> adding 1 -> 1000 (we added a new digit).
    if carry > 0:
        # We insert a '1' at the beginning of the list to represent
        # this new most significant digit.
        palindrome_digits.insert(0, "1")

        # Update the length variable because we have one more digit now.
        length += 1

    # -------------------------------------------------------------------------
    # Step 4: After incrementing the left/middle side, we mirror again.
    # -------------------------------------------------------------------------

    # Now that the left portion of the digits encodes a value that is
    # definitely big enough, we mirror it again to enforce the palindrome
    # structure on the entire number.
    mirror_from_left(palindrome_digits)

    # Join the final palindrome digit list into a string.
    final_pal_str = "".join(palindrome_digits)

    # Convert that string into an integer value.
    final_pal_value = int(final_pal_str)

    # This is our final result: the smallest palindrome strictly greater than 'num'.
    return final_pal_value


# -----------------------------------------------------------------------------
# Simple test harness using a main-like function.
# We do NOT use any testing framework, only prints.
# -----------------------------------------------------------------------------


def run_tests():
    """
    Runs a set of test cases and prints PASS/FAIL for each.
    Also includes some large-number tests.
    """

    # Each test case is a tuple of (input_number, expected_next_palindrome).
    test_cases = [
        # Basic examples from the problem statement.
        (1000, 1001),
        (1200, 1221),

        # Very small numbers.
        (0, 1),        # Next palindrome after 0 is 1.
        (1, 2),        # Next palindrome after 1 is 2.
        (8, 9),        # Next palindrome after 8 is 9.
        (9, 11),       # Next palindrome after 9 is 11.

        # Numbers that are already palindromes.
        (11, 22),      # Next after 11 is 22.
        (99, 101),     # Next after 99 is 101.
        (121, 131),    # Next after 121 is 131.

        # Mixed sizes.
        (1290, 1331),  # 1290 -> 1331.
        (1299, 1331),  # 1299 -> 1331.
        (808, 818),    # 808 -> 818.
        (999, 1001),   # 999 -> 1001.
        (9998, 9999),  # 9998 -> 9999.

        # Larger values.
        (12345, 12421),
        (54321, 54345),
    ]

    # Now we add a large-data test with many digits.
    # We create a number consisting of 100 digits of '9'.
    # For example: "999...9" (100 times).
    large_nines_str = "9" * 100
    large_nines_int = int(large_nines_str)

    # For a number of all 9s, the next palindrome after it will be
    # 10...01 (length 101, with '1' at both ends and zeros in the middle).
    expected_large_pal_str = "1" + ("0" * 99) + "1"
    expected_large_pal_int = int(expected_large_pal_str)

    # Add this big test case to our list.
    test_cases.append((large_nines_int, expected_large_pal_int))

    # Counter to track how many tests succeed.
    passed_count = 0

    # Iterate over all test cases with their index for clear printing.
    for index, (input_value, expected_value) in enumerate(test_cases, start=1):
        # Call our function to compute the next palindrome.
        result = next_palindrome_greater_than(input_value)

        # Compare the result with the expected value.
        if result == expected_value:
            # If they match, the test passes.
            print(f"Test {index}: PASS  | input={input_value}  output={result}")
            passed_count += 1
        else:
            # If they do not match, the test fails.
            print(
                f"Test {index}: FAIL  | input={input_value}  "
                f"expected={expected_value}  got={result}"
            )

    # After checking all tests, print a summary line.
    total_tests = len(test_cases)
    print(f"\nSummary: {passed_count}/{total_tests} tests passed.")


# The conventional entry point check in Python.
# When this file is run directly (not imported), the tests will execute.
if __name__ == "__main__":
    # Run our test harness to validate the implementation.
    run_tests()
