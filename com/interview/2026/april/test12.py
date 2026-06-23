def remove_duplicates(line):
    # Check if the input line is empty to avoid processing errors.
    if not line or line.strip() == "":
        return ""

    # Split the comma-separated string into a list of individual string items.
    # Example: "1,2,2,3" becomes ['1', '2', '2', '3']
    items = line.split(',')

    # Create an empty list to store the numbers we want to keep.
    unique_numbers = []

    # Loop through every single item in the split list.
    for item in items:
        # Strip away any accidental spaces and turn the string into a real integer.
        current_number = int(item.strip())

        # If unique_numbers is empty (first item) OR the current number is not equal
        # to the last number we added, it means we found a new, unique number!
        if not unique_numbers or unique_numbers[-1] != current_number:
            # Add this new unique number to our list.
            unique_numbers.append(current_number)

    # We now have a list of unique integers. We need to turn them back into a string.
    # We convert each number to a string and use ','.join() to paste them together with commas.
    result = ','.join(str(num) for num in unique_numbers)

    # Return the final cleaned-up string.
    return result


# --- Your Exact Test Cases ---

# This should print: 1,2,3,4,5
print(remove_duplicates("1,2,2,3,4,4,5"))

# This should print: 5
print(remove_duplicates("5,5,5,5,5"))