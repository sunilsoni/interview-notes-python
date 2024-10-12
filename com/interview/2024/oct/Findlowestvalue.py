def solution(numbers, nRange):
    """
    Find the lowest value in 'numbers' that falls strictly between the range in 'nRange'.

    :param numbers: List of positive integers
    :param nRange: List of two positive integers representing the range
    :return: Lowest value in range or 0 if none found
    """
    result = float('inf')
    for num in numbers:
        if nRange[0] < num < nRange[1]:
            result = min(result, num)

    return result if result != float('inf') else 0


# Test cases
def run_test_case(numbers, nRange, expected_output):
    result = solution(numbers, nRange)
    print(f"Input: numbers = {numbers}, nRange = {nRange}")
    print(f"Output: {result}")
    print(f"Expected: {expected_output}")
    print("Pass" if result == expected_output else "Fail")
    print()


# Test case 1
run_test_case([11, 4, 23, 9, 10], [5, 12], 9)

# Test case 2
run_test_case([1, 3, 2], [1, 1], 0)

# Test case 3
run_test_case([7, 23, 3, 1, 3, 5, 2], [2, 7], 3)

# Additional test cases
run_test_case([1, 2, 3, 4, 5], [3, 6], 4)
run_test_case([10, 20, 30, 40, 50], [25, 35], 30)
run_test_case([1, 1, 1, 1], [0, 2], 1)
run_test_case([5, 10, 15, 20], [1, 25], 5)
run_test_case([1, 2, 3], [4, 5], 0)
