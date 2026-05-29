def min_window(s: str, t: str) -> str:
    # Check if either string is empty; if so, a valid window is impossible
    if not t or not s:
        # Return an empty string because the requirement cannot be fulfilled
        return ""

    # Create a dictionary to keep track of how many of each character we need from string 't'
    dict_t = {}

    # Loop through every single character in the target string 't'
    for char in t:
        # Increase the count for this character by 1 (defaulting to 0 if it's the first time we see it)
        dict_t[char] = dict_t.get(char, 0) + 1

    # Store the total number of unique characters we need to match exactly
    required = len(dict_t)

    # Initialize the left pointer of our sliding window at index 0
    left = 0

    # Initialize the right pointer of our sliding window at index 0
    right = 0

    # 'formed' keeps track of how many unique characters in our window have reached the required frequency
    formed = 0

    # Create a dictionary to keep track of the character counts in our current sliding window
    window_counts = {}

    # Tuple to store our best result: (length of window, left pointer index, right pointer index)
    # We set the initial length to infinity so that any valid window we find will be smaller than it
    ans = float("inf"), None, None

    # Start a while loop to expand the window by moving the right pointer across the string 's'
    while right < len(s):
        # Extract the current character at the right edge of our window
        character = s[right]

        # Add this character to our window's dictionary, increasing its count by 1
        window_counts[character] = window_counts.get(character, 0) + 1

        # Check if the current character is one we actually need, AND if we have the exact amount needed
        if character in dict_t and window_counts[character] == dict_t[character]:
            # Since the condition is met, we have successfully formed one of the required characters
            formed += 1

        # While our window is valid (we have completely formed all required characters)
        while left <= right and formed == required:
            # Extract the character sitting at the left edge of our window (we are about to try removing it)
            character = s[left]

            # Check if the current window's length is smaller than our previously recorded smallest window
            if right - left + 1 < ans[0]:
                # If it is smaller, update our answer tuple with this new smallest length and its boundaries
                ans = (right - left + 1, left, right)

            # Shrink the window by reducing the count of the left character in our dictionary
            window_counts[character] -= 1

            # Check if removing this character caused us to fall below the required amount for this character
            if character in dict_t and window_counts[character] < dict_t[character]:
                # If it did, our window is no longer valid, so we reduce the 'formed' count
                formed -= 1

            # Move the left pointer forward by 1 space to permanently shrink the window from the left
            left += 1

        # Move the right pointer forward by 1 space to expand the window for the next iteration of the outer loop
        right += 1

    # Check if the smallest window length is still infinity (meaning we never found a valid window)
    if ans[0] == float("inf"):
        # Return an empty string because no valid window exists in string 's'
        return ""

    # If we did find a valid window, slice the original string 's' using the saved left and right boundaries
    return s[ans[1]: ans[2] + 1]


def test_solution():
    # Define a list of test cases: each tuple contains (s, t, expected_output)
    test_cases = [
        # Test Case 1: Standard case from the problem description
        ("ADOBECODEBANC", "ABC", "BANC"),
        # Test Case 2: Exact match case
        ("a", "a", "a"),
        # Test Case 3: Impossible case (not enough characters in s)
        ("a", "aa", ""),
        # Test Case 4: Target string is larger than source string
        ("abc", "abcd", ""),
        # Test Case 5: The answer is at the very beginning
        ("abcedf", "ab", "ab"),
        # Test Case 6: Duplicate characters required but separated by noise
        ("aabdec", "abc", "abdec")
    ]

    # Generate large data input for performance testing (100,000 characters)
    # String s is 100,000 'x's followed by "abc"
    large_s = ("x" * 100000) + "abc"
    # Target t is just "abc"
    large_t = "abc"
    # Expected output is just "abc" because it's the smallest window at the very end
    test_cases.append((large_s, large_t, "abc"))

    # Loop through each test case using an index for numbering
    for i, (s, t, expected) in enumerate(test_cases, 1):
        # Call our function with the current test case inputs
        result = min_window(s, t)

        # Check if the function's result matches the expected output
        if result == expected:
            # If they match, print PASS with the test case number
            print(f"Test Case {i}: PASS")
        else:
            # If they don't match, print FAIL along with what was expected vs what was returned
            print(f"Test Case {i}: FAIL | Expected: '{expected}', Got: '{result}'")


# Standard Python idiom to execute the main testing block when the script is run directly
if __name__ == "__main__":
    # Call the testing function
    test_solution()