def findRanges(nums):
    if not nums:
        return []

    result = []
    i = 0

    while i < len(nums):
        # Start of potential range
        start = nums[i]

        # Move forward while numbers are consecutive
        while i + 1 < len(nums) and nums[i + 1] == nums[i] + 1:
            i += 1

        # End of range or single number
        if start == nums[i]:
            result.append(str(start))
        else:
            result.append(f"{start}→{nums[i]}")

        i += 1

    return result


# Test cases
print(findRanges([1, 2, 3, 5, 6, 8, 9]))  # ["1→3", "5→6", "8→9"]
print(findRanges([1, 3, 5, 7]))  # ["1", "3", "5", "7"]
print(findRanges([1, 2, 3, 4, 5]))  # ["1→5"]
