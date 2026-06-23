# Import the List type for clear type hinting in our function definition.
from typing import List
# Import defaultdict from the collections module to easily group items into lists.
from collections import defaultdict


# Define the Solution class as required by the problem structure.
class Solution(object):
    # Define the method groupAnagrams that takes a list of strings and returns a list of lists of strings.
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # Create a dictionary called 'anagram_groups' where every new key automatically starts with an empty list.
        # WHY: This saves us from writing "if key not in dict: dict[key] = []" for every new word.
        anagram_groups = defaultdict(list)

        # Start a loop to process every single string (which we call 'word') inside our input list 'strs'.
        # EXAMPLE: On the first loop iteration, 'word' might be "eat".
        for word in strs:
            # Break the word into individual characters, sort them alphabetically, and return them as a list.
            # WHY: This finds the common base for all anagrams.
            # EXAMPLE: If 'word' is "eat", sorted(word) returns ['a', 'e', 't'].
            sorted_chars = sorted(word)

            # Join the sorted list of characters back together into a single string to use as a dictionary key.
            # WHY: Dictionary keys must be immutable (like strings), not lists.
            # EXAMPLE: ['a', 'e', 't'] becomes the string "aet".
            sorted_word = "".join(sorted_chars)

            # Add the original, unsorted word to the list inside the dictionary under our sorted key.
            # WHY: This groups words with the same sorted base together.
            # EXAMPLE: anagram_groups["aet"] will now contain ["eat"]. Later, it will append "tea" and "ate".
            anagram_groups[sorted_word].append(word)

        # Extract all the values (which are the grouped lists of words) from our dictionary.
        # WHY: The problem asks for a list of grouped lists, we don't need the sorted keys anymore.
        # EXAMPLE: dict_values([['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']])
        grouped_values = anagram_groups.values()

        # Convert those dictionary values into a standard Python list and return it as our final answer.
        # WHY: This satisfies the return type of List[List[str]] requested by the problem.
        return list(grouped_values)


# Define a helper function to compare two lists of lists where order doesn't matter.
# WHY: The problem says "You can return the answer in any order". We must sort the inner and outer lists to compare them accurately.
def normalize_lists(list_of_lists):
    # Sort each individual sublist, then sort the main list containing all sublists.
    return sorted([sorted(sublist) for sublist in list_of_lists])


# The main block to run our tests directly without using complex Unit Testing frameworks.
if __name__ == "__main__":
    # Create an instance of our Solution class so we can call our method.
    solution = Solution()

    # Define our test cases as a list of dictionaries containing the input and the expected output.
    test_cases = [
        # Test Case 1: Standard example provided by the problem.
        {
            "name": "Standard Example 1",
            "input": ["eat", "tea", "tan", "ate", "nat", "bat"],
            "expected": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
        },
        # Test Case 2: Dealing with empty strings.
        {
            "name": "Empty String Example 2",
            "input": [""],
            "expected": [[""]]
        },
        # Test Case 3: Dealing with single character strings.
        {
            "name": "Single Character Example 3",
            "input": ["a"],
            "expected": [["a"]]
        },
        # Test Case 4: No anagrams present at all (every word is unique).
        {
            "name": "No Anagrams Present",
            "input": ["abc", "def", "ghi"],
            "expected": [["abc"], ["def"], ["ghi"]]
        },
        # Test Case 5: Large data input to verify time constraints. 10,000 identical "a" strings.
        {
            "name": "Large Data Array",
            "input": ["a"] * 10000,
            "expected": [["a"] * 10000]
        }
    ]

    # Loop through our defined test cases one by one.
    for test in test_cases:
        # Pass the input into our function to get the actual result.
        result = solution.groupAnagrams(test["input"])

        # Normalize both the actual result and the expected result so they can be safely compared.
        normalized_result = normalize_lists(result)
        normalized_expected = normalize_lists(test["expected"])

        # Check if our normalized result exactly matches the normalized expected output.
        if normalized_result == normalized_expected:
            # If they match, print a PASS message.
            print(f"PASS: {test['name']}")
        else:
            # If they don't match, print a FAIL message and show the difference for debugging.
            print(f"FAIL: {test['name']}")
            print(f"  Expected: {test['expected']}")
            print(f"  Got:      {result}")
