def get_longest_unique_substring(text: str) -> str:
    # We define a function taking a string 'text' and returning a string (the actual substring).

    # We create an empty Set to track the unique characters currently inside our window.
    seen_chars = set()

    # We initialize the 'left' edge of our sliding window at index 0.
    left = 0

    # We initialize a variable to keep track of the maximum length found so far.
    max_length = 0

    # NEW: We add a variable to remember the exact starting index of our longest window.
    max_start = 0

    # We start a loop moving the 'right' edge of our window one character at a time.
    for right in range(len(text)):

        # We grab the current character at the 'right' position in the text.
        current_char = text[right]

        # We check if this character is already in our Set (meaning we found a duplicate rule-breaker).
        while current_char in seen_chars:
            # We identify the character sitting at the 'left' edge of the window.
            char_to_remove = text[left]

            # We remove that 'left' character from our Set because we are shrinking the window.
            seen_chars.remove(char_to_remove)

            # We move the 'left' edge one step to the right to shrink the window.
            left += 1

            # The window is now valid again, so we add the new unique 'current_char' to our Set.
        seen_chars.add(current_char)

        # We calculate the size of our currently valid window.
        current_window_size = right - left + 1

        # We check if this current window is strictly larger than our previous record.
        if current_window_size > max_length:
            # We update our record to this new, larger size.
            max_length = current_window_size

            # NEW: We save the 'left' index so we know exactly where this winning streak started.
            max_start = left

            # NEW: We slice the original string from 'max_start' to 'max_start + max_length' to get the word.
    return text[max_start: max_start + max_length]


def main():
    # We define our main testing function.

    # We create a list of test cases: (input_text, expected_string_output, description)
    test_cases = [
        # Standard case: The longest unique part is "abc" at the beginning.
        ("abcabcbb", "abc", "Standard mixed characters"),

        # Edge case: All identical characters. The longest unique part is just "b".
        ("bbbbb", "b", "All repeating characters"),

        # Standard case: The longest is "wke" in the middle.
        ("pwwkew", "wke", "Answer in the middle"),

        # Edge case: Empty string should return an empty string.
        ("", "", "Empty string"),

        # Edge case: Spaces and symbols. The longest is " !@#".
        (" !@# !@#", " !@#", "Spaces and symbols"),

        # Edge case: All unique characters. The whole string is returned.
        ("abcdefg", "abcdefg", "All unique characters")
    ]

    # We create a massive string to test large data handling.
    # 50,000 'a's, followed by "bcdef", followed by 50,000 'g's.
    # The longest unique substring will bridge the middle: "abcdefg".
    large_data_input = ("a" * 50000) + "bcdef" + ("g" * 50000)

    # We add the large data test case to our list.
    test_cases.append((large_data_input, "abcdefg", "Large data input (100,000+ chars)"))

    # We loop through all the test cases.
    for text, expected, description in test_cases:

        # We run our function and get the actual substring back.
        result = get_longest_unique_substring(text)

        # We check if the string we got matches the string we expected.
        if result == expected:
            # It matches, so we print PASS.
            print(f"PASS: {description}")
        else:
            # It failed, so we print exactly what went wrong.
            print(f"FAIL: {description}. Expected '{expected}', got '{result}'")


# Standard Python check to run the main function.
if __name__ == "__main__":
    main()