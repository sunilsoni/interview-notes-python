def findClosestElements(arr, k, x):
    # We place our first pointer at the very beginning of the array (index 0).
    left = 0

    # We place our second pointer at the very end of the array.
    # The last index is the total length of the array minus 1.
    right = len(arr) - 1

    # We loop to shrink our window until exactly 'k' elements are left.
    # The formula (right - left) gives us the number of elements in our window minus 1.
    # So, while (right - left) >= k, we have MORE than k elements, so we keep shrinking.
    while (right - left) >= k:

        # We calculate the absolute distance between the leftmost element and our target 'x'.
        # Example: if arr[left] is 1 and x is 3, abs(1 - 3) = 2.
        dist_left = abs(arr[left] - x)

        # We calculate the absolute distance between the rightmost element and our target 'x'.
        # Example: if arr[right] is 5 and x is 3, abs(5 - 3) = 2.
        dist_right = abs(arr[right] - x)

        # We check if the element on the left is further away from 'x' than the element on the right.
        if dist_left > dist_right:
            # If the left element is further, we don't want it in our final answer.
            # We shrink the window from the left by moving the pointer one step to the right.
            left += 1

        # If the right element is further away, OR if both distances are exactly the same...
        else:
            # ...we remove the right element. Why? Because the problem says if there is a tie,
            # the smaller element wins. Since the array is sorted, the smaller element is on the left.
            # We shrink the window from the right by moving the pointer one step to the left.
            right -= 1

    # The loop finishes when we have exactly 'k' elements left between 'left' and 'right'.
    # We use Python slicing to grab the elements starting from 'left' up to (left + k).
    # Slicing in Python does not include the ending index, so left + k gives us exactly k elements.
    return arr[left: left + k]


def findClosestElements(arr, k, x):
    # We place our first pointer at the very beginning of the array (index 0).
    left = 0

    # We place our second pointer at the very end of the array.
    # The last index is the total length of the array minus 1.
    right = len(arr) - 1

    # We loop to shrink our window until exactly 'k' elements are left.
    # The formula (right - left) gives us the number of elements in our window minus 1.
    # So, while (right - left) >= k, we have MORE than k elements, so we keep shrinking.
    while (right - left) >= k:

        # We calculate the absolute distance between the leftmost element and our target 'x'.
        # Example: if arr[left] is 1 and x is 3, abs(1 - 3) = 2.
        dist_left = abs(arr[left] - x)

        # We calculate the absolute distance between the rightmost element and our target 'x'.
        # Example: if arr[right] is 5 and x is 3, abs(5 - 3) = 2.
        dist_right = abs(arr[right] - x)

        # We check if the element on the left is further away from 'x' than the element on the right.
        if dist_left > dist_right:
            # If the left element is further, we don't want it in our final answer.
            # We shrink the window from the left by moving the pointer one step to the right.
            left += 1

        # If the right element is further away, OR if both distances are exactly the same...
        else:
            # ...we remove the right element. Why? Because the problem says if there is a tie,
            # the smaller element wins. Since the array is sorted, the smaller element is on the left.
            # We shrink the window from the right by moving the pointer one step to the left.
            right -= 1

    # The loop finishes when we have exactly 'k' elements left between 'left' and 'right'.
    # We use Python slicing to grab the elements starting from 'left' up to (left + k).
    # Slicing in Python does not include the ending index, so left + k gives us exactly k elements.
    return arr[left: left + k]
