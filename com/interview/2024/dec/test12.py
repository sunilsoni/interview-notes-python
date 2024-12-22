def find_zero_sum_tuples(arr1, arr2, arr3, arr4):
    # Step 1: Create a dictionary to store sums of first two arrays
    sum_dict = {}
    for a in arr1:
        for b in arr2:
            sum_ab = a + b
            sum_dict[sum_ab] = sum_dict.get(sum_ab, 0) + 1

    # Step 2: Check combinations with last two arrays
    count = 0
    for c in arr3:
        for d in arr4:
            target = -(c + d)  # We need this sum from first two arrays
            if target in sum_dict:
                count += sum_dict[target]

    return count


def run_tests():
    # Test Case 1: Given example
    test1_result = find_zero_sum_tuples([1, 2], [-2, -1], [-1, 0], [0, 2])
    print("Test 1:", "PASS" if test1_result == 3 else "FAIL")

    # Test Case 2: Empty arrays
    test2_result = find_zero_sum_tuples([], [], [], [])
    print("Test 2:", "PASS" if test2_result == 0 else "FAIL")

    # Test Case 3: Single elements
    test3_result = find_zero_sum_tuples([1], [-1], [2], [-2])
    print("Test 3:", "PASS" if test3_result == 1 else "FAIL")

    # Test Case 4: Larger arrays
    arr1 = [1, 2, 3, 4]
    arr2 = [-2, -1, 0, 1]
    arr3 = [-1, 0, 1, 2]
    arr4 = [-3, -2, -1, 0]
    test4_result = find_zero_sum_tuples(arr1, arr2, arr3, arr4)
    print("Test 4:", "PASS" if test4_result > 0 else "FAIL")


if __name__ == "__main__":
    run_tests()
