"""
Given an integer array nums, find the subarray with the largest sum, and return its sum and the subarray. A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6, [4,-1,2,1]
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
"""


def max_subarray(nums):
    max_sum = float('-inf')
    current_sum = 0
    start = 0
    end = 0
    temp_start = 0

    for i in range(len(nums)):
        current_sum += nums[i]

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

        if current_sum < 0:
            current_sum = 0
            temp_start = i + 1

    return max_sum, nums[start:end + 1]


# Example 1
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
max_subarray(nums)
