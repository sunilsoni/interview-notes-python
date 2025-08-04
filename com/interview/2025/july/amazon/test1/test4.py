def search_with_duplicates(nums, target):
    """
    Search in rotated sorted array with duplicates
    nums = [2, 2, 2, 3, 4, 2], target = 3
    """
    if not nums:
        return False

    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        # Found target
        if nums[mid] == target:
            return True

        # Handle duplicates
        if nums[left] == nums[mid] == nums[right]:
            left += 1
            right -= 1
            continue

        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return False


# Example walkthrough
def explain_with_duplicates():
    nums = [2, 2, 2, 3, 4, 2]
    target = 3

    print("Example with duplicates:")
    print(f"Array: {nums}")
    print(f"Target: {target}")

    print("\nStep by step:")

    # Step 1
    print("\nStep 1:")
    print("left = 0, right = 5, mid = 2")
    print("nums[mid] = 2")
    print("nums[left] = nums[mid] = nums[right] = 2")
    print("Skip duplicates: left++, right--")

    # Step 2
    print("\nStep 2:")
    print("left = 1, right = 4, mid = 2")
    print("nums[mid] = 2")
    print("Check right half")

    # Step 3
    print("\nStep 3:")
    print("left = 3, right = 4, mid = 3")
    print("nums[mid] = 3")
    print("Target found!")

    result = search_with_duplicates(nums, target)
    return result


# Test cases
def run_test_cases():
    test_cases = [
        ([2, 2, 2, 3, 4, 2], 3),  # With duplicates
        ([1, 1, 1, 1, 1, 2], 2),  # All same except target
        ([2, 2, 2, 2, 2], 3),  # All same, target not present
    ]

    for nums, target in test_cases:
        result = search_with_duplicates(nums, target)
        print(f"\nArray: {nums}")
        print(f"Target: {target}")
        print(f"Result: {result}")


if __name__ == "__main__":
    result = explain_with_duplicates()
    print(f"\nFinal result: {result}")
    print("\nAdditional test cases:")
    run_test_cases()
