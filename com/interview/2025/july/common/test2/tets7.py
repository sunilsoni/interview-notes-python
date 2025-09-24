def find_ocean_view_apartments(heights):
    """
    Function to find the indices of apartments with an ocean view.

    Args:
    heights (List[int]): Heights of the apartments from left to right.

    Returns:
    List[int]: Indices of apartments that can see the ocean (ascending order).
    """
    result = []  # List to store indices with ocean view
    max_height = float('-inf')  # Initialize to lowest possible value

    # Traverse from right to left
    for i in range(len(heights) - 1, -1, -1):
        # If current apartment is taller than all to its right
        if heights[i] > max_height:
            result.append(i)     # Save its index
            max_height = heights[i]  # Update max seen so far

    # Reverse the result to return in ascending order
    return result[::-1]


def main():
    # Define test cases with expected output
    test_cases = [
        {"input": [4, 3, 2, 3, 1], "expected": [0, 3, 4]},
        {"input": [1, 2, 3, 4, 5], "expected": [4]},  # only last can see ocean
        {"input": [5, 4, 3, 2, 1], "expected": [0, 1, 2, 3, 4]},  # all decreasing
        {"input": [2, 2, 2, 2], "expected": [3]},  # only last one
        {"input": [], "expected": []},  # empty input
        {"input": [1], "expected": [0]},  # single apartment
        {"input": [5, 5, 5, 1], "expected": [3]},  # only last one
        {"input": list(range(10**6, 0, -1)), "expected": list(range(10**6))}  # large decreasing input
    ]

    # Run each test case
    for idx, test in enumerate(test_cases):
        result = find_ocean_view_apartments(test["input"])
        status = "PASS" if result == test["expected"] else "FAIL"
        print(f"Test {idx + 1}: {status}")
        print(f"  Input:    {test['input'][:10]}{'...' if len(test['input']) > 10 else ''}")
        print(f"  Expected: {test['expected'][:10]}{'...' if len(test['expected']) > 10 else ''}")
        print(f"  Got:      {result[:10]}{'...' if len(result) > 10 else ''}")
        print("-" * 50)

if __name__ == "__main__":
    main()