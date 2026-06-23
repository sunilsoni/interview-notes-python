# Import List to provide type hints so our code is easy to read and understand.
from typing import List
# Import defaultdict to automatically create an empty list if a key doesn't exist yet.
from collections import defaultdict


# Define the Solution class as required by the problem format.
class Solution(object):
    # Define the method that takes a list of strings and returns a list of grouped strings.
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:

        # Create our dictionary to group words. New keys automatically get an empty list.
        # WHY: This avoids having to write extra logic to check if a key already exists.
        anagram_groups = defaultdict(list)

        # Start a loop to look at every single string in our input list.
        # EXAMPLE: Let's pretend the current 'word' we are looking at is "cat".
        for word in strs:

            # Create a tally array of exactly 26 zeros, representing 'a' through 'z'.
            # WHY: This gives us a blank slate to count the letters for the current word.
            char_counts = [0] * 26

            # Loop through each individual letter in the current word.
            # EXAMPLE: For "cat", we look at 'c', then 'a', then 't'.
            for char in word:
                # Calculate the mathematical index (0 to 25) for the letter.
                # WHY: ord('c') - ord('a') gives us index 2.
                alphabet_index = ord(char) - ord('a')
                # Add 1 to our tally at that specific index.
                # EXAMPLE: The tally at index 2 (which represents 'c') becomes 1.
                char_counts[alphabet_index] += 1

            # Create an empty list to help us build your custom string key.
            # WHY: Appending to a list and joining it at the end is the fastest way to build strings in Python.
            key_builder = []

            # Loop through all 26 possible letter indices in our tally.
            # WHY: Looping from 0 to 25 enforces alphabetical order ('a' first, then 'b', etc.).
            for i in range(26):

                # Check if the count for the current letter is greater than zero.
                # WHY: We only want to add letters that actually exist in the word, skipping empty ones.
                if char_counts[i] > 0:
                    # Convert the index back into its actual English letter.
                    # WHY: chr(i + ord('a')) reverses our math. If i is 2, this turns it back into 'c'.
                    actual_letter = chr(i + ord('a'))

                    # Fetch the number of times this letter appeared from our tally.
                    # EXAMPLE: For 'c' in "cat", this number is 1.
                    letter_count = char_counts[i]

                    # Add the letter and its count to our builder list as a formatted string.
                    # EXAMPLE: This adds "c1" to the list.
                    key_builder.append(f"{actual_letter}{letter_count}")

            # Join all the little strings in our list together into one single string.
            # WHY: This creates your final custom key!
            # EXAMPLE: The list ["a1", "c1", "t1"] becomes the single string "a1c1t1".
            string_key = "".join(key_builder)

            # Group the original word into our dictionary using your custom string key.
            # WHY: "cat" and "act" both generate "a1c1t1", so they both get put into this same list.
            anagram_groups[string_key].append(word)

        # Extract all the lists of words from the dictionary and return them.
        # WHY: We just need the groupings for the final answer, we don't need the string keys anymore.
        return list(anagram_groups.values())


# Helper function to sort lists so we can easily compare actual vs expected outputs.
# WHY: The problem allows returning the answer in any order, so we normalize the lists before comparing.
def normalize_lists(list_of_lists):
    # Sort the words in each group, then sort the main list of groups.
    return sorted([sorted(sublist) for sublist in list_of_lists])


# Main method to act as our simple test runner.
if __name__ == "__main__":
    # Create the solution object.
    solution = Solution()

    # Define our testing scenarios.
    test_cases = [
        {
            "name": "Standard Example",
            "input": ["eat", "tea", "tan", "ate", "nat", "bat"],
            "expected": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
        },
        {
            "name": "Your Example (cat/act)",
            "input": ["cat", "bat", "act"],
            "expected": [["bat"], ["act", "cat"]]
        },
        {
            "name": "Empty String Example",
            "input": [""],
            "expected": [[""]]
        },
        {
            "name": "Large Data Inputs (10,000 identical words)",
            "input": ["a"] * 10000,
            "expected": [["a"] * 10000]
        }
    ]

    # Loop through and run each test.
    for test in test_cases:
        result = solution.groupAnagrams(test["input"])

        # Normalize the outputs to compare them fairly.
        normalized_result = normalize_lists(result)
        normalized_expected = normalize_lists(test["expected"])

        # Check if they match.
        if normalized_result == normalized_expected:
            print(f"PASS: {test['name']}")
        else:
            print(f"FAIL: {test['name']}")
            print(f"  Expected: {test['c']}")
            print(f"  Got:      {result}")
