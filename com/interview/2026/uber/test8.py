from collections import deque  # We use deque because it supports O(1) pops from both ends.


def longest_n_stable_subarray_length(arr, n):
    # Purpose:
    # Return the length of the longest contiguous subarray such that:
    # max(subarray) - min(subarray) <= n

    if n < 0:
        # Reason:
        # For any non-empty subarray, max-min is always >= 0.
        # If n is negative, it is impossible to satisfy max-min <= n.
        return 0

    if not arr:
        # Reason:
        # No elements -> no non-empty subarray exists.
        # Return 0 by convention for "longest length".
        return 0

    min_dq = deque()
    # min_dq stores indices of elements in increasing order of their values.
    # The front (min_dq[0]) always points to the smallest value in current window.

    max_dq = deque()
    # max_dq stores indices of elements in decreasing order of their values.
    # The front (max_dq[0]) always points to the largest value in current window.

    left = 0
    # left is the start index of the current sliding window.

    best = 0
    # best stores the maximum valid window length we have seen so far.

    for right in range(len(arr)):
        # right is the end index of the sliding window.
        # We expand the window by adding arr[right].

        x = arr[right]
        # Store current element in x to avoid repeating arr[right] many times.

        # ----------------------------------------------------
        # Maintain min_dq (monotonic increasing by value)
        # ----------------------------------------------------
        while min_dq and arr[min_dq[-1]] > x:
            # If the last element in min_dq is bigger than x,
            # then that last element can NEVER be the minimum anymore
            # for any window that includes x (because x is smaller and newer).
            min_dq.pop()
            # Remove it from consideration to keep deque increasing.

        min_dq.append(right)
        # Add current index.
        # It becomes a candidate minimum for current/future windows.

        # ----------------------------------------------------
        # Maintain max_dq (monotonic decreasing by value)
        # ----------------------------------------------------
        while max_dq and arr[max_dq[-1]] < x:
            # If the last element in max_dq is smaller than x,
            # then that last element can NEVER be the maximum anymore
            # for any window that includes x (because x is bigger and newer).
            max_dq.pop()
            # Remove it so deque stays decreasing.

        max_dq.append(right)
        # Add current index as a candidate maximum.

        # ----------------------------------------------------
        # Shrink window from left if it violates max-min <= n
        # ----------------------------------------------------
        while arr[max_dq[0]] - arr[min_dq[0]] > n:
            # max is at max_dq[0], min is at min_dq[0].
            # If max-min > n, the window is invalid (not N-stable).
            # We must shrink from the left to reduce range.

            if min_dq[0] == left:
                # If the minimum element index is exactly the left boundary,
                # moving left forward means that minimum leaves the window.
                min_dq.popleft()
                # Remove it because it is no longer inside [left..right].

            if max_dq[0] == left:
                # Same logic for maximum element leaving window.
                max_dq.popleft()

            left += 1
            # Move left forward by 1 step (shrink window).
            # We repeat until the window becomes valid.

        # ----------------------------------------------------
        # Window is valid here, update best
        # ----------------------------------------------------
        window_len = right - left + 1
        # Length formula for inclusive window [left..right].

        if window_len > best:
            # If current valid window is larger, record it.
            best = window_len

    return best
    # After scanning all right positions, best is the answer.
