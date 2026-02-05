import collections


def longest_n_stable_subarray(nums, N):
    # If the input array is empty, the answer is 0.
    if not nums:
        return 0

    # 'max_q' will store INDICES of numbers in a way that the biggest number is always at the front (index 0).
    # We use a 'deque' (double-ended queue) because we need to remove items from both ends efficiently.
    max_q = collections.deque()

    # 'min_q' will store INDICES of numbers in a way that the smallest number is always at the front.
    min_q = collections.deque()

    # 'left' is the pointer for the start of our sliding window.
    left = 0

    # 'max_len' keeps track of the longest valid subarray length found so far.
    max_len = 0

    # We loop through the array using 'right' as the end pointer of our sliding window.
    # enumerate gives us both the index (right) and the value (num).
    for right, num in enumerate(nums):

        # 1. Maintain the Max Deque (Decreasing order)
        # If the new number 'num' is bigger than numbers currently at the back of max_q,
        # those numbers can never be the maximum again (because 'num' is bigger and to their right).
        # So, we remove them (pop).
        while max_q and nums[max_q[-1]] <= num:
            max_q.pop()
        # Add the current index to the max queue.
        max_q.append(right)

        # 2. Maintain the Min Deque (Increasing order)
        # If the new number 'num' is smaller than numbers currently at the back of min_q,
        # those numbers can never be the minimum again. So, we remove them.
        while min_q and nums[min_q[-1]] >= num:
            min_q.pop()
        # Add the current index to the min queue.
        min_q.append(right)

        # 3. Check Condition: Is (Max - Min) > N?
        # max_q[0] holds the index of the largest value in the current window.
        # min_q[0] holds the index of the smallest value in the current window.
        while max_q and min_q and (nums[max_q[0]] - nums[min_q[0]] > N):
            # If the difference is too big, the window is invalid.
            # We must shrink the window from the left to exclude the element causing the issue.
            left += 1

            # After moving 'left', we check if the current Max or Min is now outside the window.
            # If the index at the front of max_q is less than 'left', it's no longer in our subarray.
            if max_q[0] < left:
                max_q.popleft()
            # Same check for the min_q.
            if min_q[0] < left:
                min_q.popleft()

        # 4. Update Result
        # The window [left, right] is now valid. Calculate its length.
        # Length = right - left + 1. We keep the larger of current max_len or this new length.
        current_len = right - left + 1
        if current_len > max_len:
            max_len = current_len

    return max_len


# --- Test Method ---

def run_tests():
    print("Starting Tests...\n")

    # Test Case 1: The example from the image
    # Subarray [2, 2, 3, 2] is valid (Max 3 - Min 2 = 1 <= 1). Length 4.
    nums1 = [4, 2, 3, 6, 2, 2, 3, 2, 7]
    n1 = 1
    expected1 = 4
    result1 = longest_n_stable_subarray(nums1, n1)
    status1 = "PASS" if result1 == expected1 else f"FAIL (Got {result1})"
    print(f"Test 1 (Image Example): {status1}")

    # Test Case 2: Array with single element
    # A single element has difference 0, which is always <= N (assuming N >= 0).
    nums2 = [10]
    n2 = 5
    expected2 = 1
    result2 = longest_n_stable_subarray(nums2, n2)
    status2 = "PASS" if result2 == expected2 else f"FAIL (Got {result2})"
    print(f"Test 2 (Single Element): {status2}")

    # Test Case 3: No valid pair (N=0, elements distinct)
    # Only single elements are valid here.
    nums3 = [1, 5, 10, 20]
    n3 = 0
    expected3 = 1
    result3 = longest_n_stable_subarray(nums3, n3)
    status3 = "PASS" if result3 == expected3 else f"FAIL (Got {result3})"
    print(f"Test 3 (Distinct N=0):  {status3}")

    # Test Case 4: All elements same
    # Max - Min is always 0. The whole array is valid.
    nums4 = [5, 5, 5, 5, 5]
    n4 = 2
    expected4 = 5
    result4 = longest_n_stable_subarray(nums4, n4)
    status4 = "PASS" if result4 == expected4 else f"FAIL (Got {result4})"
    print(f"Test 4 (All Same):      {status4}")

    # Test Case 5: Large Data Input
    # We generate 100,000 numbers. This checks if the solution is O(N) efficient.
    # If the logic was O(N^2), this would hang or take very long.
    import random
    # Create a list like [0, 1, 2, 3... 100000]
    # With N=100000, the whole array is stable because Max(100k)-Min(0) <= 100k.
    large_nums = list(range(100000))
    large_n = 100000
    expected_large = 100000

    # Timing the execution roughly
    import time
    start_time = time.time()
    result_large = longest_n_stable_subarray(large_nums, large_n)
    end_time = time.time()

    status_large = "PASS" if result_large == expected_large else f"FAIL (Got {result_large})"
    print(f"Test 5 (Large Input):   {status_large} - Time taken: {end_time - start_time:.4f} seconds")

    print("\nAll tests completed.")


if __name__ == "__main__":
    run_tests()