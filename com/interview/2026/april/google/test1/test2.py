def largest_subsequence_number(s, k):  # Function name: returns the largest number possible by choosing k digits in order.
    n = len(s)  # Total number of digits in the input string; used often, so store it once.

    if k == 0:  # Special case: if we need to pick 0 digits.
        return ""  # The only valid subsequence of length 0 is an empty string.

    if k >= n:  # Special case: if k is equal to or more than total digits.
        return s  # We cannot remove digits and still keep order, so return the whole string.

    stack = []  # This will store chosen digits; we use it like a stack (last in, first out).

    for i, digit in enumerate(s):  # Read each digit from left to right along with its position.
        # We try to improve the answer by removing smaller digits from the end of the stack.
        # Why? Because a larger digit earlier gives a larger final number.
        #
        # Conditions:
        # 1) stack must not be empty, otherwise there is nothing to remove
        # 2) last chosen digit must be smaller than current digit, otherwise removing is useless
        # 3) after removing one digit, we must still be able to build exactly k digits total
        #
        # len(stack) - 1  -> size after popping one digit
        # (n - i)         -> count of digits from current position to end, including current digit
        # total available after pop = len(stack) - 1 + (n - i)
        # if that total is still >= k, popping is safe
        while stack and stack[-1] < digit and len(stack) - 1 + (n - i) >= k:  # Keep removing weaker previous digits while it is safe and helpful.
            stack.pop()  # Remove the last smaller digit because current bigger digit makes the number better.

        stack.append(digit)  # Add current digit into our chosen structure.

    # After scanning all digits, stack may contain more than k digits.
    # That can happen because sometimes we do not have a reason to pop.
    # In that case, the best answer is simply the first k digits from stack.
    return "".join(stack[:k])  # Convert the first k chosen digits back into a string result.


def largest_subsequence_number(s, k):  # Function to compute the largest subsequence of length k.
    n = len(s)  # Save input size for repeated use.

    if k == 0:  # If no digits are needed.
        return ""  # Return empty string.

    if k >= n:  # If we need all digits or more than available.
        return s  # Return full string.

    stack = []  # List used as a stack to build the best answer greedily.

    for i, digit in enumerate(s):  # Process each digit from left to right.
        while stack and stack[-1] < digit and len(stack) - 1 + (n - i) >= k:  # Remove smaller previous digits when safe.
            stack.pop()  # Popping makes room for a better bigger digit earlier.

        stack.append(digit)  # Add current digit after required removals.

    return "".join(stack[:k])  # Final answer is the first k digits from the built stack.


def run_one_test(test_id, s, k, expected):  # Helper function to run one test case and print PASS or FAIL.
    actual = largest_subsequence_number(s, k)  # Call the solution for this test.
    status = "PASS" if actual == expected else "FAIL"  # Compare actual answer with expected answer.
    print(f"Test {test_id}: {status}")  # Print test result label.
    print(f"  Input   : S={s}, K={k}")  # Show input used for the test.
    print(f"  Expected: {expected}")  # Show expected answer.
    print(f"  Actual  : {actual}")  # Show actual answer from the code.
    print()  # Print a blank line to keep output easy to read.


def run_large_test():  # Separate function for a large input performance-style test.
    s = "1234567890" * 20000  # Create a large string of 200,000 digits to test scalability.
    k = 100000  # Ask for a large subsequence length to make sure logic works on big data.
    ans = largest_subsequence_number(s, k)  # Run the solution on the large input.
    ok = len(ans) == k  # Basic correctness check: result must contain exactly k digits.
    print("Large Test:", "PASS" if ok else "FAIL")  # Print whether large test passed.
    print(f"  Input length : {len(s)}")  # Show total size of input.
    print(f"  Output length: {len(ans)}")  # Show size of produced answer.
    print()  # Blank line for readable output.


if __name__ == "__main__":  # Standard Python entry point so tests run only when file is executed directly.
    run_one_test(1, "375924", 3, "974")  # Mixed digits case.
    run_one_test(2, "987654", 3, "987")  # Already decreasing, best is first k digits.
    run_one_test(3, "123456", 3, "456")  # Increasing order, best is last k digits.
    run_one_test(4, "11111", 3, "111")  # All digits same.
    run_one_test(5, "102030", 3, "230")  # Includes zeroes.
    run_one_test(6, "9", 1, "9")  # Single digit input.
    run_one_test(7, "54321", 5, "54321")  # k equals n.
    run_one_test(8, "54321", 0, "")  # k is zero.
    run_one_test(9, "765028321", 4, "8321")  # General mixed case.
    run_one_test(10, "100200300", 4, "2300")  # More zero-heavy case.

    run_large_test()  # Run one large data test to confirm it handles big inputs.