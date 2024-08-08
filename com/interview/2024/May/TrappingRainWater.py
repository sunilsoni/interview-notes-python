from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        n = len(height)
        left_max = [0] * n
        right_max = [0] * n

        left_max[0] = height[0]
        for i in range(1, n):
            left_max[i] = max(left_max[i - 1], height[i])

        right_max[n - 1] = height[n - 1]
        for i in range(n - 2, -1, -1):
            right_max[i] = max(right_max[i + 1], height[i])

        water = 0
        for i in range(n):
            water += min(left_max[i], right_max[i]) - height[i]

        return water


def main():
    # Example 1
    height1 = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    solution = Solution()
    result1 = solution.trap(height1)
    print(f"Example 1 Output: {result1}")
    assert result1 == 6, "Example 1 failed"

    # Example 2
    height2 = [4, 2, 0, 3, 2, 5]
    result2 = solution.trap(height2)
    print(f"Example 2 Output: {result2}")
    assert result2 == 9, "Example 2 failed"

    # Additional test cases
    # Test case 3: Empty array
    height3 = []
    result3 = solution.trap(height3)
    print(f"Test case 3 Output: {result3}")
    assert result3 == 0, "Test case 3 failed"

    # Test case 4: Single element array
    height4 = [5]
    result4 = solution.trap(height4)
    print(f"Test case 4 Output: {result4}")
    assert result4 == 0, "Test case 4 failed"

    # Test case 5: Descending heights
    height5 = [5, 4, 3, 2, 1]
    result5 = solution.trap(height5)
    print(f"Test case 5 Output: {result5}")
    assert result5 == 0, "Test case 5 failed"

    # Test case 6: Ascending heights
    height6 = [1, 2, 3, 4, 5]
    result6 = solution.trap(height6)
    print(f"Test case 6 Output: {result6}")
    assert result6 == 0, "Test case 6 failed"

    print("All test cases passed!")


if __name__ == "__main__":
    main()
