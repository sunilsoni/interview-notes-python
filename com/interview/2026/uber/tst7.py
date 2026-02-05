from collections import deque  # We use deque to maintain min/max in O(1) amortized time.


def longest_n_stable_subarray_length(arr, n):
    # This function returns the length of the longest subarray where max(subarray)-min(subarray) <= n.

    if n < 0:  # If n is negative, even a single element (diff 0) won't satisfy 0 <= n.
        return 0  # So no valid non-empty subarray exists.

    if not arr:  # If the array is empty,
        return 0  # then the longest valid subarray length is 0.

    min_dq = deque()  # This will store indices of elements in increasing order of values (front is min).
    max_dq = deque()  # This will store indices of elements in decreasing order of values (front is max).

    left = 0  # Left boundary of the sliding window.
    best = 0  # We store the best (maximum) window length found so far.

    for right in range(len(arr)):  # Move right boundary from 0 to end of array.
        x = arr[right]  # Current value being added to the window.

        # --- Maintain min_dq (increasing values) ---
        # We remove indices from the back while they have values bigger than current x,
        # because x is smaller and will be a better minimum for future windows.
        while min_dq and arr[min_dq[-1]] > x:
            min_dq.pop()  # Remove worse (bigger) value index from the back.
        min_dq.append(right)  # Add current index; it may become the new minimum.

        # --- Maintain max_dq (decreasing values) ---
        # We remove indices from the back while they have values smaller than current x,
        # because x is bigger and will be a better maximum for future windows.
        while max_dq and arr[max_dq[-1]] < x:
            max_dq.pop()  # Remove worse (smaller) value index from the back.
        max_dq.append(right)  # Add current index; it may become the new maximum.

        # Now the window is [left..right], but it may be invalid.
        # We keep shrinking from the left until max-min <= n.
        while arr[max_dq[0]] - arr[min_dq[0]] > n:  # If window violates the rule,
            # If the index leaving the window is currently the min index, remove it.
            if min_dq[0] == left:
                min_dq.popleft()  # Remove old min because it is no longer inside window.

            # If the index leaving the window is currently the max index, remove it.
            if max_dq[0] == left:
                max_dq.popleft()  # Remove old max because it is no longer inside window.

            left += 1  # Move left boundary rightward to shrink the window.

        # At this point, the window is valid again.
        # Update best length if this window is longer than previous best.
        window_len = right - left + 1  # Length of current valid window.
        if window_len > best:  # If it is better than what we had,
            best = window_len  # store it.

    return best  # Return the maximum length found.


def brute_force_longest(arr, n):
    # Slow correctness checker for small arrays only (O(n^2)).
    # It tries all subarrays and checks max-min.
    if n < 0:
        return 0
    best = 0
    for i in range(len(arr)):
        mn = arr[i]
        mx = arr[i]
        for j in range(i, len(arr)):
            if arr[j] < mn:
                mn = arr[j]
            if arr[j] > mx:
                mx = arr[j]
            if mx - mn <= n:
                length = j - i + 1
                if length > best:
                    best = length
    return best


def run_test(test_name, arr, n, expected):
    # Runs one test and prints PASS/FAIL.
    got = longest_n_stable_subarray_length(arr, n)  # Compute answer using fast method.
    if got == expected:  # Compare with expected answer.
        print(f"PASS: {test_name} -> {got}")  # Print pass message.
    else:
        print(f"FAIL: {test_name} -> expected {expected}, got {got}")  # Print fail message.


def main():
    # -----------------------------
    # Provided-style example test
    # -----------------------------
    run_test(
        "example_N_1",
        [4, 2, 3, 6, 2, 2, 3, 2, 7],
        1,
        4
    )

    # -----------------------------
    # Simple edge cases
    # -----------------------------
    run_test("single_element", [10], 0, 1)  # One element always stable if n >= 0.
    run_test("empty_array", [], 5, 0)       # Empty array returns 0.
    run_test("n_negative", [1, 1, 1], -1, 0)  # No valid subarray if n < 0.

    # N=0 means all elements in window must be equal (max-min=0)
    run_test("all_equal_n0", [5, 5, 5, 5], 0, 4)
    run_test("mixed_n0", [1, 1, 2, 2, 2, 1], 0, 3)  # Longest block of same number is 3.

    # -----------------------------
    # More correctness tests
    # -----------------------------
    run_test("increasing_n2", [1, 2, 3, 4, 5], 2, 3)  # e.g., [1,2,3] max-min=2 length 3
    run_test("random_small_known", [8, 5, 6, 7, 3, 4], 2, 3)

    # -----------------------------
    # Random small stress (fast vs brute) to catch bugs
    # -----------------------------
    import random  # Used only for generating test data.

    random.seed(7)  # Fixed seed so results are repeatable.

    ok = True  # Track if all stress checks pass.
    for t in range(200):  # Run multiple random tests.
        size = random.randint(0, 40)  # Small size so brute force is fine.
        arr = [random.randint(-10, 10) for _ in range(size)]  # Random values.
        n = random.randint(0, 10)  # Non-negative N.
        fast = longest_n_stable_subarray_length(arr, n)  # Fast answer.
        slow = brute_force_longest(arr, n)  # Brute force answer.
        if fast != slow:  # If mismatch found,
            ok = False  # mark failure,
            print("FAIL: stress_mismatch")
            print("arr =", arr)
            print("n =", n)
            print("fast =", fast, "slow =", slow)
            break  # Stop early; we found an error.

    if ok:  # If no mismatches in stress tests,
        print("PASS: stress_tests (fast == brute for 200 random cases)")

    # -----------------------------
    # Large input performance test (no brute here)
    # -----------------------------
    # This test is only to show it runs fast on big data.
    large_n = 3  # Allowed range of values inside window.
    large_arr = [random.randint(0, 1_000_000) for _ in range(200_000)]  # 200k elements.
    ans = longest_n_stable_subarray_length(large_arr, large_n)  # Should run in O(n).
    print("INFO: large_test_done, result_length =", ans)


if __name__ == "__main__":
    main()
