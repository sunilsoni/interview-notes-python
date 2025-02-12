def find_largest_square(cityLine):
    if not cityLine:
        return 0

    n = len(cityLine)
    max_side = min(n, min(cityLine))  # Maximum possible square side

    for size in range(max_side, 0, -1):
        # Check each possible position for square
        for start in range(n - size + 1):
            can_fit = True
            # Check if square can fit at current position
            for i in range(start, start + size):
                if cityLine[i] < size:
                    can_fit = False
                    break
            if can_fit:
                return size * size
    return 1


def run_tests():
    # Test cases
    test_cases = [
        # Basic test cases
        ([4, 3, 4], 9),
        ([1, 2, 3, 2, 1], 4),
        ([1], 1),
        ([5, 5], 4),
        # Edge cases
        ([], 0),
        ([1000000] * 5, 25),  # Large numbers
        ([1] * 1000000, 1),  # Large array
    ]

    for i, (input_data, expected) in enumerate(test_cases):
        result = find_largest_square(input_data)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i + 1}: {status}")
        print(f"Input: {input_data[:10]}{'...' if len(input_data) > 10 else ''}")
        print(f"Expected: {expected}")
        print(f"Got: {result}\n")


if __name__ == "__main__":
    run_tests()
