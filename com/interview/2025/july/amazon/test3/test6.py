def find_ranges(nums):
    # Handle empty input case
    if not nums:
        return []

    # Initialize result list to store ranges
    ranges = []

    # Initialize start of current range with first number
    start = nums[0]

    # Initialize previous number with first number
    prev = nums[0]

    # Iterate through numbers starting from second element
    for num in nums[1:]:
        # If current number is not consecutive to previous
        if num != prev + 1:
            # Add the completed range to results
            if start == prev:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}→{prev}")
            # Start new range from current number
            start = num
        # Update previous number for next iteration
        prev = num

    # Handle the last range
    if start == prev:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}→{prev}")

    return ranges


# Main method for testing
def main():
    # Test cases with expected outputs
    test_cases = [
        ([1, 2, 3, 5, 6, 8, 9], ["1→3", "5→6", "8→9"]),
        ([1], ["1"]),
        ([1, 3, 5, 7], ["1", "3", "5", "7"]),
        ([1, 2, 3, 4, 5], ["1→5"]),
        ([], []),
        ([1, 2, 4, 5, 7, 8, 9, 10], ["1→2", "4→5", "7→10"])
    ]

    # Process each test case
    for i, (input_arr, expected) in enumerate(test_cases, 1):
        result = find_ranges(input_arr)
        passed = result == expected
        print(f"Test {i}: {'PASS' if passed else 'FAIL'}")
        print(f"Input: {input_arr}")
        print(f"Expected: {expected}")
        print(f"Got: {result}\n")


# Run tests
if __name__ == "__main__":
    main()
