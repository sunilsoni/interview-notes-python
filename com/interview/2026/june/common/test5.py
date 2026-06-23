# Import List for type hinting.
from typing import List
# Import defaultdict to automatically handle empty lists for new dictionary keys.
from collections import defaultdict


# Define our Solution class.
class Solution(object):
    # Define our method that takes the list of strings.
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:

        # Create our dictionary to group the anagrams.
        # WHY: defaultdict prevents "KeyError" by automatically creating an empty list for new keys.
        anagram_groups = defaultdict(list)

        # Start processing each word from our input list one by one.
        # EXAMPLE: First word might be "eat".
        for word in strs:

            # Create a list of exactly 26 zeros to represent the counts of 'a' through 'z'.
            # WHY: This creates a blank slate to tally up the letters for the current word.
            # EXAMPLE: [0, 0, 0, 0, 0, 0, ...] (26 zeros total).
            char_counts = [0] * 26

            # Loop through every single character inside the current word.
            # EXAMPLE: For "eat", we will look at 'e', then 'a', then 't'.
            for char in word:
                # Calculate the correct index (0 to 25) for the current character.
                # WHY: ord() gets the mathematical ASCII value of a character.
                # Subtracting ord('a') shifts the value so 'a' becomes index 0, 'b' becomes 1, etc.
                # EXAMPLE: If char is 'e', ord('e') - ord('a') gives us index 4.
                alphabet_index = ord(char) - ord('a')

                # Increment the tally at that specific index by 1.
                # WHY: This records that we have found one instance of this letter.
                # EXAMPLE: The zero at index 4 becomes a 1.
                char_counts[alphabet_index] += 1

            # Convert our fully tallied list of 26 numbers into a Python tuple.
            # WHY: Lists can be changed (mutable), so Python forbids them as dictionary keys.
            # Tuples are locked (immutable), so they work perfectly as keys.
            # EXAMPLE: tuple(char_counts) might look like (1, 0, 0, 0, 1, ..., 1, ...)
            count_signature = tuple(char_counts)

            # Use our unique tuple signature to group the original word in the dictionary.
            # WHY: Anagrams will generate the exact same tuple signature, placing them in the same list.
            anagram_groups[count_signature].append(word)

        # Extract all the lists of grouped words from the dictionary and return them.
        # WHY: We only care about the groupings, we no longer need the tuple keys.
        return list(anagram_groups.values())


# Helper function to sort nested lists so we can accurately verify if our code PASSES.
# WHY: The output order doesn't matter per the rules, so we must normalize it before checking equality.
def normalize_lists(list_of_lists):
    # Sort the words inside each group, then sort the groups themselves.
    return sorted([sorted(sublist) for sublist in list_of_lists])


# Main block to act as our test runner.
if __name__ == "__main__":
    # Initialize the solution.
    solution = Solution()

    # Define our test scenarios, including a massive data test.
    test_cases = [
        {
            "name": "Standard Example 1",
            "input": ["eat", "tea", "tan", "ate", "nat", "bat"],
            "expected": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
        },
        {
            "name": "Empty String Example 2",
            "input": [""],
            "expected": [[""]]
        },
        {
            "name": "Single Character Example 3",
            "input": ["a"],
            "expected": [["a"]]
        },
        {
            "name": "No Anagrams Present",
            "input": ["abc", "def", "ghi"],
            "expected": [["abc"], ["def"], ["ghi"]]
        },
        {
            "name": "Large Data Array (10k items)",
            "input": ["a"] * 10000,
            "expected": [["a"] * 10000]
        }
    ]

    # Process each test case.
    for test in test_cases:
        # Run the optimized function.
        result = solution.groupAnagrams(test["input"])

        # Normalize outputs for a fair comparison.
        normalized_result = normalize_lists(result)
        normalized_expected = normalize_lists(test["expected"])

        # Print PASS or FAIL.
        if normalized_result == normalized_expected:
            print(f"PASS: {test['name']}")
        else:
            print(f"FAIL: {test['name']}")
            print(f"  Expected: {test['expected']}")
            print(f"  Got:      {result}")
