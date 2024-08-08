def find_elements_more_than_n_over_k(array, k):
    n = len(array)
    threshold = n // k
    count_map = {}
    output = []

    for num in array:
        if num in count_map:
            count_map[num] += 1
        else:
            count_map[num] = 1

    for key, value in count_map.items():
        if value > threshold:
            output.append(key)

    return output
