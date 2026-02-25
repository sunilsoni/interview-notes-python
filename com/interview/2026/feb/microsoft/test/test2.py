def get_longest_unique_substring_length(text: str) -> int:
    # We define a function taking a string named 'text' and returning an integer.

    # We create an empty Set called 'seen_chars'.
    # A Set is a simple data structure that stores unique items and checks for duplicates instantly.
    seen_chars = set()

    # We create a variable to point to the left side of our 'sliding window'. It starts at index 0.
    left = 0

    # We create a variable to keep track of the maximum length we have found so far. It starts at 0.
    max_length = 0

    # We start a loop where 'right' is the index of the right side of our window, moving through the string.
    for right in range(len(text)):

        # We grab the actual character at the 'right' index of the text.
        current_char = text[right]

        # We check if this current character is ALREADY inside our 'seen_chars' Set (meaning it's a duplicate).
        while current_char in seen_chars:
            # If it is a duplicate, we find the character currently sitting at the 'left' edge of our window.
            char_to_remove = text[left]

            # We remove that 'left' character from our Set because it is about to fall out of our window.
            seen_chars.remove(char_to_remove)

            # We move the left edge of our window one step to the right to shrink the window.
            left += 1

            # Now that all duplicates are removed, we add our new, unique 'current_char' to the Set.
        seen_chars.add(current_char)

        # We calculate the current window's size (right - left + 1).
        current_window_size = right - left + 1

        # If this current window is bigger than our recorded 'max_length', we update 'max_length'.
        if current_window_size > max_length:
            # We save the new record for the largest window size we've seen so far.
            max_length = current_window_size

            # After the loop finishes checking the whole string, we return the highest maximum length we found.
    return max_length


def main():
    # We define our main function where we will run all our tests.

    # We create a list of test cases. Each item is a tuple: (input_string, expected_output, description).
    test_cases = [
        # Standard case with mixed duplicates
        ("abcabcbb", 3, "Standard mixed characters"),

        # Edge case: All identical characters
        ("bbbbb", 1, "All repeating characters"),

        # Standard case where longest is in the middle
        ("pwwkew", 3, "Answer in the middle"),

        # Edge case: Empty string
        ("", 0, "Empty string"),

        # Edge case: String with spaces and symbols
        (" !@# !@#", 4, "Spaces and symbols"),

        # Edge case: All unique characters
        ("abcdefg", 7, "All unique characters")
    ]

    # We generate a massive string for the Large Data test to prove our code won't crash or run forever.
    # It creates 50,000 'a's, followed by 'bcdef', followed by 50,000 'g's.
    # The longest unique part is "abcdefg" which is length 7.
    large_data_input = ("a" * 50000) + "bcdef" + ("g" * 50000)

    # We add this large data case to our list of tests.
    test_cases.append((large_data_input, 7, "Large data input (100,000+ chars)"))

    # We start a loop to go through each test case one by one.
    for text, expected, description in test_cases:

        # We call our function with the test string and store the result.
        result = get_longest_unique_substring_length(text)

        # We check if the result our function gave matches what we expected.
        if result == expected:

            # If it matches, we print a PASS message with the description.
            print(f"PASS: {description}")

        else:

            # If it fails, we print a FAIL message showing what went wrong.
            print(f"FAIL: {description}. Expected {expected}, got {result}")


# This is a standard Python way to say "If this script is run directly, execute the main() function".
if __name__ == "__main__":
    main()