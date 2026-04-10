def find_largest_subsequence(S: str, K: int) -> str:
    # We will use a simple list as a 'stack' to keep track of the best digits we choose.
    stack = []

    # We calculate the total length of the sequence S and store it in variable 'n'.
    n = len(S)

    # We start a loop to go through every single character in the sequence by its index 'i'.
    for i in range(n):

        # We extract the digit at the current index 'i' and save it to a variable.
        current_digit = S[i]

        # We calculate how many digits are left to process, including the current one.
        # This is vital to know if we can afford to discard smaller digits.
        digits_left = n - i

        # Now we enter a 'while' loop to see if we should remove previously chosen digits.
        # Condition 1: 'stack' checks if the stack is not empty (we need something to compare to).
        # Condition 2: 'stack[-1] < current_digit' checks if the last chosen digit is smaller than the new one.
        # Condition 3: '(len(stack) - 1 + digits_left) >= K' checks if we discard the last digit,
        # do we still have enough digits left in the original string to hit our target length of K?
        while stack and stack[-1] < current_digit and (len(stack) - 1 + digits_left) >= K:
            # If all three conditions are true, the previous digit is making our number smaller.
            # So, we remove (pop) the smaller digit from the end of the stack.
            stack.pop()

        # After removing any smaller, unhelpful digits, we check if our stack needs more digits.
        # If the length of our stack is currently less than our target length K:
        if len(stack) < K:
            # We add the current, newly evaluated digit to the end of our stack.
            stack.append(current_digit)

    # Finally, our stack contains the best characters in a list format (e.g., ['9', '3']).
    # We use the join function to glue them together into a single string (e.g., "93").
    return "".join(stack)


def main():
    # We define a list of test cases. Each test case is a tuple containing:
    # (Original_Sequence, K_Length, Expected_Result)
    test_cases = [
        # Basic test cases to verify standard functionality
        ("312", 2, "32"),
        ("913", 2, "93"),
        ("12345", 3, "345"),
        ("54321", 3, "543"),
        ("9876543210", 5, "98765"),

        # Edge case: K is exactly the length of the string (must return the exact string)
        ("492", 3, "492"),

        # Edge case: Sequence contains duplicate digits
        ("82828", 3, "888"),

        # Large Data Input Case:
        # A string of "1928" repeated 50,000 times (total length 200,000 characters).
        # If we want the largest 4 digits, it should greedily pick four '9's from across the string.
        ("1928" * 50000, 4, "9999")
    ]

    # We initialize a counter to track test numbers
    test_number = 1

    # We loop through every test case in our list
    for S, K, expected in test_cases:

        # We call our function with the sequence and K
        result = find_largest_subsequence(S, K)

        # We check if our function's result matches the expected correct answer
        if result == expected:
            # If it matches, the test passes
            print(f"Test {test_number} PASS: S={S[:15]}... K={K} | Got: {result}")
        else:
            # If it doesn't match, the test fails
            print(f"Test {test_number} FAIL: S={S[:15]}... K={K} | Expected: {expected}, Got: {result}")

        # Increment the test number for the next loop
        test_number += 1


# This block ensures the main function runs when the script is executed
if __name__ == "__main__":
    main()