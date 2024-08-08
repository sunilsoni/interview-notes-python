def remove_consecutive_k_or_more_elements(arr, k):
    if k <= 1:
        return arr

    result = []
    count = 1

    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1]:
            count += 1
        else:
            if count < k:  # Add previous section if it didn't reach k consecutive elements
                result.extend([arr[i - 1]] * count)
            count = 1  # Reset count for the new element

    # Handle the last sequence
    if count < k:
        result.extend([arr[-1]] * count)

    return result


# Example usage
array = [1, 2, 2, 3, 3, 3, 2]
k = 3
output = remove_consecutive_k_or_more_elements(array, k)
print(output)  # [1, 2, 1]
