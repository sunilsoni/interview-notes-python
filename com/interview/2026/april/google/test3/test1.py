def get_maximum_subarray_indices(arr):
    # Same base validation
    if not arr or len(arr) < 2:
        raise ValueError("Invalid input: Array must contain at least 2 elements.")

    # Same initial mathematical setup
    max_score = float('-inf')
    max_v = arr[0]

    # --- NEW: Breadcrumb variables to track indices ---
    current_start = 0  # Tracks where the currently active subarray started
    best_start = -1  # Locks in the start index of the highest scoring subarray
    best_end = -1  # Locks in the end index of the highest scoring subarray

    for i in range(1, len(arr)):
        # Calculate the score ending at the current element
        current_score = max_v + arr[i]

        # If this score beats our record...
        if current_score > max_score:
            # We save the new high score
            max_score = current_score
            # AND we lock in the exact indices that created it
            best_start = current_start
            best_end = i

        # Update max_v for the next iteration
        if arr[i] > (max_v - arr[i]):
            # Starting fresh provides a better value.
            max_v = arr[i]
            # --- NEW: Because we started a new subarray, update our start tracker
            current_start = i
        else:
            # Extending provides a better value.
            max_v = max_v - arr[i]
            # We DO NOT update current_start here because we are just continuing the existing chain.

    # Return the start and end indices of the absolute best subarray
    return [best_start, best_end]


import unittest


# --- The Function Being Tested ---
def get_maximum_subarray_score(arr):
    if not arr or len(arr) < 2:
        raise ValueError("Invalid input: Array must contain at least 2 elements.")

    max_score = float('-inf')
    max_v = arr[0]

    for i in range(1, len(arr)):
        current_score = max_v + arr[i]

        if current_score > max_score:
            max_score = current_score

        if arr[i] > (max_v - arr[i]):
            max_v = arr[i]
        else:
            max_v = max_v - arr[i]

    return max_score


# --- The Unit Test Suite ---
class TestMaximumSubarrayScore(unittest.TestCase):

    def test_happy_path(self):
        # General mixed array
        self.assertEqual(get_maximum_subarray_score([3, 1, 2, 5, 4]), 9)
        # Small positive array
        self.assertEqual(get_maximum_subarray_score([3, 1, 2, 5]), 7)

    def test_invalid_inputs(self):
        # Empty array should raise ValueError
        with self.assertRaises(ValueError):
            get_maximum_subarray_score([])

        # Single element array should raise ValueError
        with self.assertRaises(ValueError):
            get_maximum_subarray_score([5])

    def test_boundary_conditions(self):
        # Minimum valid length (no intermediate elements)
        self.assertEqual(get_maximum_subarray_score([10, 20]), 30)

        # Large dataset stress test (100,000 ones)
        large_array = [1] * 100000
        self.assertEqual(get_maximum_subarray_score(large_array), 2)

    def test_mathematical_edge_cases(self):
        # All negative numbers
        # Max subarray is [-1, -2, -3] -> -1 + (-3) - (-2) = -2
        self.assertEqual(get_maximum_subarray_score([-5, -1, -2, -3]), -2)

        # All zeroes
        self.assertEqual(get_maximum_subarray_score([0, 0, 0, 0]), 0)

        # Negative intermediate values (which actually add to the score)
        # 5 + 5 - (-10) = 20
        self.assertEqual(get_maximum_subarray_score([5, -10, 5]), 20)


if __name__ == '__main__':
    unittest.main()

def main():
    arr = [3, 1, 2, 5, 4]

    # Call our new function
    indices = get_maximum_subarray_indices(arr)

    print(f"Original Array: {arr}")
    print(f"Best Indices Found: {indices}")

    # You can use standard Python slicing to easily grab the actual subarray using those indices
    start_idx = indices[0]
    end_idx = indices[1]

    # We add +1 to end_idx because Python slices stop BEFORE the second number
    best_subarray = arr[start_idx: end_idx + 1]

    print(f"Actual Subarray: {best_subarray}")


if __name__ == "__main__":
    main()