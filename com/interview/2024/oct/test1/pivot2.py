"""

Python3 Task:

You are given an array of integers numbers and an integer pivot
Your task is to return a new array in which the ith element equals:
• 0 if numbers[i] is zero.
• 1 if numbers[i] and pivot have the same sign (both positive or both negative).
• -1 if numbers[i] and pivot have different signs.
Note: It is guaranteed that pivot isn't equal to zero. Also note that you are not expected to provide the most optimal solution, but a solution with time complexity not worse than (numbers. length?) will fit within the execution time limit.
Example
• For numbers = [6, -5, 0] and pivot = 2, the output should be solution (numbers, pivot) = [1, -1, 0J -
The returned array output should look as follows:
• output [0] = 1 because numbers [0] = 6 , which has the same sign as pivot = 2
• output [1] = -1 because numbers [1] = -5, which has a different sign than pivot = 2
• output [2] = 0 because numbers [2] = 0 .
Input/Output
• [execution time limit] 4 seconds (py3)
• [memory limit] 1 GB
• [input] array.integer numbers
An array of integers.
Guaranteed constraints:
1 ≤ numbers. length ≤ 1000 ,
-109 ≤ numbers [i] ≤ 10 power 9
• [input] integer pivot
An integer for comparison. It is guaranteed that pivot isn't equal to zero.

• [input] integer pivot
An integer for comparison. It is guaranteed that pivot isn't equal to zero.
Guaranteed constraints:
-109 ≤ pivot ≤ 109
pivot = 0 .
• [output] array.integer
Return a new array, where the jth element is 0, 1, or -1, based on the algorithm described in the task.

def solution (numbers, pivot):
"""
def solution(numbers, pivot):
    """
    This function takes an array of integers 'numbers' and an integer 'pivot', and returns a new array where:
    - The ith element is 0 if numbers[i] is zero.
    - The ith element is 1 if numbers[i] and pivot have the same sign.
    - The ith element is -1 if numbers[i] and pivot have different signs.
    """
    result = []
    for num in numbers:
        if num == 0:
            result.append(0)
        elif (num > 0 and pivot > 0) or (num < 0 and pivot < 0):
            result.append(1)
        else:
            result.append(-1)
    return result

def run_tests():
    """
    This function runs a series of test cases to verify the correctness of the 'solution' function.
    It prints 'PASS' if the test case passes, and 'FAIL' along with details if it fails.
    """
    test_cases = [
        # Test case 1: Example from the problem description
        ([6, -5, 0], 2, [1, -1, 0]),

        # Test case 2: All zeros in numbers
        ([0, 0, 0], 1, [0, 0, 0]),

        # Test case 3: Negative numbers with negative pivot
        ([-1, -2, -3], -5, [1, 1, 1]),

        # Test case 4: Positive numbers with negative pivot
        ([1, 2, 3], -1, [-1, -1, -1]),

        # Test case 5: Mixed zeros and non-zeros
        ([0, -1, 1], 1, [0, -1, 1]),

        # Test case 6: Large data input
        ([i for i in range(-500, 500)], -100,
         [0 if i == 0 else (1 if i < 0 else -1) for i in range(-500, 500)]),

        # Test case 7: Pivot is positive, numbers range from negative to positive
        ([i for i in range(-10, 11)], 5,
         [0 if i == 0 else (1 if i > 0 else -1) for i in range(-10, 11)]),

        # Test case 8: Pivot is negative, numbers range from negative to positive
        ([i for i in range(-10, 11)], -5,
         [0 if i == 0 else (1 if i < 0 else -1) for i in range(-10, 11)]),

        # Test case 9: Single element in numbers
        ([0], 3, [0]),
        ([-1000000000], 1, [-1]),
        ([1000000000], -1, [-1]),

        # Test case 10: Numbers equal to pivot
        ([2, -2, 0], 2, [1, -1, 0]),
        ([-3, 3, 0], -3, [1, -1, 0]),
    ]

    all_passed = True

    for idx, (numbers, pivot, expected) in enumerate(test_cases):
        output = solution(numbers, pivot)
        if output == expected:
            print(f"Test case {idx+1}: PASS")
        else:
            all_passed = False
            print(f"Test case {idx+1}: FAIL")
            print(f"  Input numbers: {numbers}")
            print(f"  Input pivot: {pivot}")
            print(f"  Expected output: {expected}")
            print(f"  Actual output:   {output}")

    if all_passed:
        print("\nAll test cases passed!")
    else:
        print("\nSome test cases failed.")

if __name__ == "__main__":
    run_tests()
