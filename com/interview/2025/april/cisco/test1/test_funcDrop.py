def funcDrop(xCoordinate, yCoordinate):
    from collections import Counter

    # Count occurrences of each x and y
    x_count = Counter(xCoordinate)
    y_count = Counter(yCoordinate)

    # Get the maximum occurrences
    max_x = max(x_count.values())
    max_y = max(y_count.values())

    # Return the maximum of the two
    return max(max_x, max_y)


def test_funcDrop():
    tests = [
        {"x": [2, 3, 2, 4, 2], "y": [2, 2, 6, 5, 8], "expected": 3},
        {"x": [1, 2], "y": [3, 4], "expected": 1},  # All unique
        {"x": [1, 1, 1], "y": [2, 3, 4], "expected": 3},  # Vertical line
        {"x": [1, 2, 3], "y": [4, 4, 4], "expected": 3},  # Horizontal line
        {"x": [1, 2, 3, 1, 2, 1], "y": [3, 3, 3, 4, 4, 4], "expected": 3},  # Equal count in x and y
    ]

    passed = 0
    for i, test in enumerate(tests):
        result = funcDrop(test["x"], test["y"])
        print(
            f"Test {i + 1}: {'PASS' if result == test['expected'] else 'FAIL'} - Expected: {test['expected']} Got: {result}")
        if result == test['expected']:
            passed += 1

    print(f"{passed}/{len(tests)} Tests Passed")


if __name__ == "__main__":
    test_funcDrop()
