def get_maximum_subarray_score(arr):
    # Check if the array exists and has at least 2 elements because a valid subarray needs a first and last element.
    if not arr or len(arr) < 2:
        # If the input is invalid, we return None as calculating a score is impossible here.
        return None

    # Initialize max_score to negative infinity to ensure that the very first valid score we calculate will replace it.
    max_score = float('-inf')

    # Initialize max_v with the first element; this represents the best "first element minus intermediates" starting condition.
    max_v = arr[0]

    # Start a loop from the second element (index 1) to the end of the array to evaluate every possible subarray end.
    for i in range(1, len(arr)):

        # Calculate the score ending at the current element by adding it to our best running open subarray state (max_v).
        current_score = max_v + arr[i]

        # Check if the newly calculated current_score is strictly greater than our historically highest recorded max_score.
        if current_score > max_score:
            # If it is greater, we replace max_score with current_score so we never lose track of the maximum found.
            max_score = current_score

        # We must now update max_v for the NEXT iteration. We have two choices: start fresh or extend the current subarray.
        # We calculate (max_v - arr[i]) which represents extending the subarray by treating the current element as an intermediate.
        # We compare this against just arr[i], which represents starting a brand-new length-2 subarray on the next turn.
        if arr[i] > (max_v - arr[i]):

            # Starting fresh provides a larger mathematical value for the next step, so we reset max_v to the current element.
            max_v = arr[i]

        else:
            # Extending the previous sequence provides a better value, so we update max_v by subtracting the current element.
            max_v = max_v - arr[i]

    # After the loop finishes checking all elements, we return the absolute maximum score we found.
    return max_score


def run_test_case(test_name, input_arr, expected_output):
    # Call our logic function and store the result
    result = get_maximum_subarray_score(input_arr)

    # Check if the result matches our mathematical expectation
    if result == expected_output:
        # Print a clear PASS message if the logic worked flawlessly
        print(f"PASS - {test_name}: Expected {expected_output}, Got {result}")
    else:
        # Print a clear FAIL message so we know exactly which test broke and what it outputted
        print(f"FAIL - {test_name}: Expected {expected_output}, Got {result}")


def main():
    # Print a header to easily identify the start of the test suite execution
    print("--- Starting Test Suite ---")

    # Test Case 1: The general example based on the prompt's array (the max subarray is actually [5, 4] -> 5+4 = 9)
    run_test_case("General Case", [3, 1, 2, 5, 4], 9)

    # Test Case 2: A smaller subset from the prompt's example. Max subarray is [2, 5] -> 2+5 = 7
    run_test_case("Small Positive Array", [3, 1, 2, 5], 7)

    # Test Case 3: All negative numbers to ensure the math doesn't break. Max subarray is [-1, -2] -> -1 + -2 = -3
    run_test_case("All Negative Numbers", [-5, -1, -2, -3], -3)

    # Test Case 4: Array with exactly two elements. Only one subarray possible. Score is 10 + 20 = 30
    run_test_case("Minimum Length Array", [10, 20], 30)

    # Test Case 5: Testing with intermediate numbers being highly negative (which actually increases the score)
    run_test_case("Negative Intermediates", [10, -5, 10, -5, 10], 25)

    # Test Case 6: Large Data Input. An array of 100,000 ones. Max score of any subarray will just be 1 + 1 = 2
    large_array_ones = [1] * 100000
    run_test_case("Large Data - All Ones", large_array_ones, 2)

    # Test Case 7: Large Data Input with alternating values to stress test the state changes
    large_array_alternating = [5, -5] * 50000
    # The max subarray will be [5, -5, 5] -> 5 + 5 - (-5) = 15
    run_test_case("Large Data - Alternating", large_array_alternating, 15)


# Standard Python idiom to trigger the main testing function only when the script is run directly
if __name__ == "__main__":
    main()