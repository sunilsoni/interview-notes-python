def solution(operations):
    # Initialize variables to store the minimum of rectangle sorted sides
    min_s0 = float('inf')
    min_s1 = float('inf')
    result = []

    for op in operations:
        op_type, a, b = op
        if op_type == 0:
            # Add rectangle
            s_rect = sorted([a, b])
            min_s0 = min(min_s0, s_rect[0])
            min_s1 = min(min_s1, s_rect[1])
        elif op_type == 1:
            # Query
            s_box = sorted([a, b])
            if s_box[0] <= min_s0 and s_box[1] <= min_s1:
                result.append(True)
            else:
                result.append(False)
    return result

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

    # Test case 4: Corrected expected output
    operations = [[0, 100, 200], [0, 150, 100], [1, 100, 150], [1, 200, 100]]
    expected = [True, False]  # Corrected expected output
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
