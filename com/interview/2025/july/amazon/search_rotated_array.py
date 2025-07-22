"""
### 🔍 Problem: Search in Sorted and Rotated Array

1. Given a **sorted and rotated** array of **distinct integers**, write a function to **search for a given integer**.

Return the **index of the integer if found**, **else return `-1`**.

---

### 🧮 Example

**Sorted array before rotation:**
`[1, 2, 3, 5, 6, 7, 8, 9, 10]`

**Input:**
`array = [5, 6, 7, 8, 9, 10, 1, 2, 3, 4]`, `target = 3`

**Output:**
`8`

---
"""


def search_rotated_array(arr, target):
    # Handle empty array case
    if not arr:
        return -1

    # Initialize left and right pointers
    left, right = 0, len(arr) - 1

    while left <= right:
        # Calculate middle point
        mid = (left + right) // 2

        # If target found at mid, return index
        if arr[mid] == target:
            return mid

        # Check if left half is sorted
        if arr[left] <= arr[mid]:
            # Check if target lies in left half
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half must be sorted
        else:
            # Check if target lies in right half
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1

    # Target not found
    return -1


def test_search_rotated_array():
    print("Running test cases...")

    # Test case 1: Normal case
    test1 = [5, 6, 7, 8, 9, 10, 1, 2, 3, 4]
    result = search_rotated_array(test1, 3)
    print(f"Test 1: Search for 3 in {test1}")
    print(f"Expected: 8, Got: {result}")
    assert result == 8, "Test 1 Failed"

    # Test case 2: Target at start
    test2 = [5, 1, 2, 3, 4]
    result = search_rotated_array(test2, 5)
    print(f"\nTest 2: Search for 5 in {test2}")
    print(f"Expected: 0, Got: {result}")
    assert result == 0, "Test 2 Failed"

    # Test case 3: Target at end
    test3 = [3, 4, 5, 1, 2]
    result = search_rotated_array(test3, 2)
    print(f"\nTest 3: Search for 2 in {test3}")
    print(f"Expected: 4, Got: {result}")
    assert result == 4, "Test 3 Failed"

    # Test case 4: Not found
    test4 = [4, 5, 6, 1, 2, 3]
    result = search_rotated_array(test4, 7)
    print(f"\nTest 4: Search for 7 in {test4}")
    print(f"Expected: -1, Got: {result}")
    assert result == -1, "Test 4 Failed"

    # Test case 5: Empty array
    test5 = []
    result = search_rotated_array(test5, 1)
    print(f"\nTest 5: Search for 1 in empty array")
    print(f"Expected: -1, Got: {result}")
    assert result == -1, "Test 5 Failed"

    # Test case 6: Large array
    # Creating a large rotated array: [500...999, 0...499]
    test6 = list(range(500, 1000)) + list(range(0, 500))
    target = 250
    expected = 750  # 250 will be at index 750 in the rotated array
    result = search_rotated_array(test6, target)
    print(f"\nTest 6: Search for {target} in large rotated array")
    print(f"Expected: {expected}, Got: {result}")
    assert result == expected, "Test 6 Failed"

    print("\nAll test cases passed successfully!")


if __name__ == "__main__":
    test_search_rotated_array()
