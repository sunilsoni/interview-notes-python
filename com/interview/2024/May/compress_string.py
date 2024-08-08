def compress_string(input_str):
    if not input_str:
        return ""

    compressed = ""
    count = 1
    prev_char = input_str[0]

    for char in input_str[1:]:
        if char == prev_char:
            count += 1
        else:
            compressed += str(count) + prev_char
            count = 1
            prev_char = char

    compressed += str(count) + prev_char
    return compressed


# Example usage:
input_str = 'aaabbcccd'
output_str = compress_string(input_str)
print(output_str)  # Output: 3a4b3c1d
