def process_list(lst, k):
    if k <= 1:
        return []

    stack = []

    for num in lst:
        if stack and stack[-1][0] == num:
            stack[-1][1] += 1
        else:
            if stack and stack[-1][1] >= k:
                stack.pop()
            stack.append([num, 1])

    if stack and stack[-1][1] >= k:
        stack.pop()

    result = []
    for elem, count in stack:
        result.extend([elem] * count)

    return result


# Transposing utility function
def transpose(matrix):
    return list(map(list, zip(*matrix)))


# Main function processing 2D array
def remove_consecutive_k_or_more_elements_2d(matrix, k):
    # Process Rows
    processed_matrix = [process_list(row, k) for row in matrix]

    # Transpose, process Columns, then transpose back
    transposed_matrix = transpose(processed_matrix)
    processed_transposed_matrix = [process_list(col, k) for col in transposed_matrix]

    # Transpose back to original layout
    fully_processed_matrix = transpose(processed_transposed_matrix)

    return fully_processed_matrix


# Example usage
matrix = [
    [1, 2, 2, 3],
    [3, 3, 3, 2],
    [1, 1, 1, 1],
    [2, 2, 3, 3]
]
k = 3
output = remove_consecutive_k_or_more_elements_2d(matrix, k)
for row in output:
    print(row)
