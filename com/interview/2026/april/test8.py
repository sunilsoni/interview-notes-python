def min_window(s: str, t: str) -> str:
    # Initialize an empty dictionary to hold the character frequencies required from string 't'
    dict_t = {}

    # Loop through each character in the target string 't' to record its required count
    for char in t:
        # Increment the count of the character, defaulting to 0 if it's not yet in the dictionary
        dict_t[char] = dict_t.get(char, 0) + 1

    # Set the starting index of the left boundary of our sliding window to 0
    left = 0
    # Set the starting index of the right boundary of our sliding window to 0
    right = 0
    # Initialize a counter to track how many unique characters have met their required frequency in the window
    counter = 0
    # Create an empty dictionary to store the counts of characters inside our current sliding window
    window_counts = {}
    # Store the number of unique characters in 't' that need to be fully matched
    required = len(dict_t)
    # Initialize the minimum window length found so far to infinity so any valid window will be smaller
    global_minima = float('inf')
    # Initialize 'ans' as an empty string to hold our final substring result
    ans = ""

    # Start a loop to expand the window by moving the 'right' pointer to the end of string 's'
    while right < len(s):
        # Pick the character currently at the 'right' pointer position
        character = s[right]
        # Add this character to our current window count dictionary, incrementing its frequency by 1
        window_counts[character] = window_counts.get(character, 0) + 1

        # Check if this character is needed AND if its count in our window exactly matches its required count in 't'
        if character in dict_t and window_counts[character] == dict_t[character]:
            # We successfully matched the frequency for one unique character, so increment our counter
            counter += 1

        # Enter a loop to shrink the window from the left as long as the current window remains valid
        while left <= right and counter == required:
            # Pick the character currently at the 'left' pointer position
            character = s[left]

            # Check if the current window length (right - left + 1) is smaller than our global minimum length
            if global_minima > right - left + 1:
                # Update our global minimum length with this new smaller window size
                global_minima = right - left + 1
                # Extract and store the actual substring slice from 's' between the left and right pointers
                ans = s[left:right + 1]

            # Since we are about to shrink the window, decrease the frequency count of the left character
            window_counts[character] -= 1

            # Check if removing this character makes its count drop below what is required by 't'
            if character in dict_t and window_counts[character] < dict_t[character]:
                # The window is no longer completely valid for this character, so decrement our counter
                counter -= 1

            # Move the left pointer forward by 1 step to officially shrink our window boundary
            left += 1

        # Move the right pointer forward by 1 step to expand our window boundary in the next iteration
        right += 1

    # Return the smallest valid substring found throughout the entire process
    return ans


# Test the function with the exact example provided at the bottom of the screenshot
print(min_window("ADOBECODEBAANC", "ABC"))