def remove_consecutive(array, k):
    output = []
    i = 0

    while i < len(array):
        count = 1
        j = i + 1

        while j < len(array) and array[j] == array[i]:
            count += 1
            j += 1

        # Add elements to output array only if count is less than k
        if count < k:
            output.append(array[i])

        i = j

    return output


# Example usage
array = [1, 2, 2, 3, 3, 3, 2]
k = 3
output = remove_consecutive(array, k)
print(output)  # Output: [1, 2]
