def solution(operations):
    """
    Solves the rectangle fitting problem.

    Args:
    operations (List[List[int]]): A list of operations, where each operation is a list of three integers.

    Returns:
    List[bool]: A list of booleans representing the answers to the query operations.
    """
    # Initialize variables to store the minimum of rectangle min sides and max sides
    min_rect_min = float('inf')
    min_rect_max = float('inf')
    result = []

    for op in operations:
        op_type, a, b = op
        if op_type == 0:
            # Add rectangle
            rect_min = min(a, b)
            rect_max = max(a, b)
            min_rect_min = min(min_rect_min, rect_min)
            min_rect_max = min(min_rect_max, rect_max)
        elif op_type == 1:
            # Query
            box_min = min(a, b)
            box_max = max(a, b)
            if box_min <= min_rect_min and box_max <= min_rect_max:
                result.append(True)
            else:
                result.append(False)
    return result


# Test cases to verify the solution

def test_solution():
    # Test case 1: No rectangles added yet, query should return True
    operations = [[1, 1, 1]]
    expected = [True]
    assert solution(operations) == expected, f"Test case 1 failed: expected {expected}, got {solution(operations)}"
    print("Test case 1 passed.")

    # Test case 2: Only rectangles added, no queries, result should be empty
    operations = [[0, 100000, 100000]]
    expected = []
    assert solution(operations) == expected, f"Test case 2 failed: expected {expected}, got {solution(operations)}"
    print("Test case 2 passed.")

    # Test case 3: Example provided in the problem description
    operations = [[0, 3, 3], [0, 5, 2], [1, 3, 2], [1, 2, 4]]
    expected = [True, False]
    assert solution(operations) == expected, f"Test case 3 failed: expected {expected}, got {solution(operations)}"
    print("Test case 3 passed.")

    # Test case 4: Additional test case
    operations = [[0, 100, 200], [0, 150, 100], [1, 100, 150], [1, 200, 100]]
    expected = [True, True]
    assert solution(operations) == expected, f"Test case 4 failed: expected {expected}, got {solution(operations)}"
    print("Test case 4 passed.")

    # Test case 5: Large data test case
    operations = [[0, 100000, 100000]] * 100000 + [[1, 100000, 100000]]
    expected = [True]
    assert solution(operations) == expected, "Test case 5 failed: Large data test case"
    print("Test case 5 passed.")

    print("All test cases passed.")


# Run the test cases
test_solution()
